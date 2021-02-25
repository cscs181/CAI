"""Application Client Class.

This module is used to control client actions.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import string
import struct
import secrets
import asyncio
from hashlib import md5
from typing import Any, List, Dict, Union, Optional, Callable

from rtea import qqtea_decrypt

from .login import (
    encode_login_request, decode_login_response, OICQResponse, LoginSuccess,
    NeedCaptcha, AccountFrozen, DeviceLocked, TooManySMSRequest,
    DeviceLockLogin, UnknownLoginStatus
)

from cai.exceptions import (
    ApiResponseError, LoginException, LoginSliderNeeded, LoginCaptchaNeeded,
    LoginAccountFrozen, LoginDeviceLocked, LoginSMSRequestError
)

from cai.log import logger
from .siginfo import SigInfo
from .packet import IncomingPacket
from cai.utils.binary import Packet
from cai.utils.future import FutureStore
from .event import Event, _packet_to_event
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol
from cai.connection import connect, Connection
from .sso_server import get_sso_server, SsoServer

DEVICE = get_device()
APK_INFO = get_protocol()
HANDLERS: Dict[str, Callable[[IncomingPacket], Event]] = {
    "wtlogin.login": decode_login_response
}


class Client:

    def __init__(self, uin: int, password_md5: bytes):
        # account info
        self._uin: int = uin
        self._password_md5: bytes = password_md5
        self._nick: Optional[str] = None
        self._age: Optional[int] = None
        self._gender: Optional[int] = None
        self._friend_list: List[Any] = []
        self._group_list: List[Any] = []
        self._other_clients: List[Any] = []

        self._seq: int = 0x3635
        self._key: bytes = secrets.token_bytes(16)
        self._session_id: bytes = bytes([0x02, 0xB0, 0x5B, 0x8B])
        self._connection: Optional[Connection] = None

        self._g: bytes = bytes()
        self._time_diff: int = 0
        self._dpwd: bytes = bytes()
        self._ksid: bytes = bytes()
        self._pwd_flag: bool = False
        self._rand_seed: bytes = bytes()
        self._rollback_sig: bytes = bytes()

        self._t104: bytes = bytes()
        self._t108: bytes = bytes()
        self._t149: bytes = bytes()
        self._t150: bytes = bytes()
        self._t174: bytes = bytes()
        self._t402: bytes = bytes()
        self._t528: bytes = bytes()
        self._t530: bytes = bytes()

        self._siginfo: SigInfo = SigInfo()
        self._receive_store: FutureStore[int, Event] = FutureStore()

    @property
    def uin(self) -> int:
        return self._uin

    @property
    def nick(self) -> Optional[str]:
        return self._nick

    @property
    def age(self) -> Optional[int]:
        return self._age

    @property
    def gender(self) -> Optional[int]:
        return self._gender

    @property
    def connection(self) -> Connection:
        if not self._connection or self._connection.closed:
            raise ConnectionError(
                "Lost Connection! Use `connect` or `reconnect` first."
            )
        return self._connection

    @property
    def connected(self) -> bool:
        return bool(self._connection) and not self._connection.closed

    async def connect(self, server: Optional[SsoServer] = None) -> None:
        if self.connected:
            raise RuntimeError("Already connected to the server")

        _server = server or await get_sso_server()
        try:
            self._connection = await connect(
                _server.host, _server.port, ssl=False, timeout=3.
            )
            asyncio.create_task(self.receive())
        except ConnectionError as e:
            raise
        except Exception as e:
            raise ConnectionError(
                "An error occurred while connecting to "
                f"server({_server.host}:{_server.port}): " + repr(e)
            )

    async def disconnect(self) -> None:
        if self._connection:
            await self._connection.close()

    async def reconnect(
        self,
        change_server: bool = False,
        server: Optional[SsoServer] = None
    ) -> None:
        if not change_server and self._connection:
            await self._connection.reconnect()
            return

        exclude = [self._connection.host] if self._connection else []
        _server = server or await get_sso_server(
            cache=False, cache_server_list=True, exclude=exclude
        )
        await self.disconnect()
        await self.connect(_server)

    async def close(self):
        await self.disconnect()

    @property
    def seq(self) -> int:
        return self._seq

    def next_seq(self) -> int:
        self._seq = (self._seq + 1) % 0x7FFF
        return self._seq

    def _send(self, packet: Union[bytes, Packet]) -> None:
        self.connection.write_bytes(packet)

    async def send_and_wait(
        self,
        seq: int,
        command_name: str,
        packet: Union[bytes, Packet],
        timeout: Optional[float] = 10.
    ) -> Event:
        logger.debug(f"--> {seq}: {command_name}")
        self._send(packet)
        return await self._receive_store.fetch(seq, timeout)

    async def receive(self):
        """Receive data from connection reader and store it in sequence future.

        Note:
            Source: com.tencent.mobileqq.msf.core.auth.n.a
        """
        while self.connected:
            try:
                length: int = struct.unpack(
                    ">i", await self.connection.read_bytes(4)
                )[0] - 4
                # FIXME: length < 0 ?
                data = await self.connection.read_bytes(length)
                packet = IncomingPacket.parse(
                    data, self._key, self._siginfo.d2key,
                    self._siginfo.wt_session_ticket_key
                )
                logger.debug(
                    f"<-- {packet.seq} ({packet.ret_code}): {packet.command_name}"
                )
                handler = HANDLERS.get(packet.command_name, _packet_to_event)
                packet = handler(packet)
                self._receive_store.store_result(packet.seq, packet)
                # TODO: broadcast packet
            except ConnectionAbortedError:
                logger.debug("Connection closed")
            except Exception as e:
                # TODO: handle exception
                logger.exception(e)

    async def login(self) -> OICQResponse:
        seq = self.next_seq()
        packet = encode_login_request(
            seq, self._key, self._session_id, self.uin, self._password_md5
        )
        response = await self.send_and_wait(seq, "wtlogin.login", packet)
        if not isinstance(response, OICQResponse):
            raise RuntimeError("Invalid login response type!")

        if not isinstance(response, UnknownLoginStatus):
            raise ApiResponseError(
                response.uin, response.seq, response.ret_code,
                response.command_name
            )

        if response.t402:
            self._dpwd = (
                "".join(
                    secrets.choice(string.ascii_letters + string.digits)
                    for _ in range(16)
                )
            ).encode()
            self._t402 = response.t402
            self._g = md5(DEVICE.guid + self._dpwd + self._t402).digest()

        if isinstance(response, LoginSuccess):
            self._t150 = response.t150 or self._t150
            self._rollback_sig = response.rollback_sig or self._rollback_sig
            self._rand_seed = response.rand_seed or self._rand_seed
            self._time_diff = response.time_diff or self._time_diff
            self._t149 = response.t149 or self._t149
            self._t528 = response.t528 or self._t528
            self._t530 = response.t530 or self._t530
            self._ksid = response.ksid or self._ksid
            self._pwd_flag = response.pwd_flag or self._pwd_flag
            self._nick = response.nick or self._nick
            self._age = response.age or self._age
            self._gender = response.gender or self._gender

            self._siginfo.tgt = response.tgt or self._siginfo.tgt
            self._siginfo.tgt_key = response.tgt_key or self._siginfo.tgt_key
            self._siginfo.srm_token = response.srm_token or self._siginfo.srm_token
            self._siginfo.t133 = response.t133 or self._siginfo.t133
            self._siginfo.encrypted_a1 = (
                response.encrypted_a1 or self._siginfo.encrypted_a1
            )
            self._siginfo.user_st_key = response.user_st_key or self._siginfo.user_st_key
            self._siginfo.user_st_web_sig = (
                response.user_st_web_sig or self._siginfo.user_st_web_sig
            )
            self._siginfo.s_key = response.s_key or self._siginfo.s_key
            self._siginfo.s_key_expire_time = (
                response.s_key_expire_time or self._siginfo.s_key_expire_time
            )
            self._siginfo.d2 = response.d2 or self._siginfo.d2
            self._siginfo.d2key = response.d2key or self._siginfo.d2key
            self._siginfo.wt_session_ticket_key = (
                response.wt_session_ticket_key or
                self._siginfo.wt_session_ticket_key
            )
            self._siginfo.device_token = (
                response.device_token or self._siginfo.device_token
            )
            self._siginfo.ps_key_map = response.ps_key_map or self._siginfo.ps_key_map
            self._siginfo.pt4_token_map = (
                response.pt4_token_map or self._siginfo.pt4_token_map
            )

            key = md5(
                self._password_md5 + bytes(4) + struct.pack(">I", self._uin)
            ).digest()
            decrypted = qqtea_decrypt(response.encrypted_a1, key)
            DEVICE.tgtgt = decrypted[51:67]
            logger.info(f"{self.nick}({self.uin}) 登录成功！")
        elif isinstance(response, NeedCaptcha):
            if response.verify_url:
                logger.info(f"登录失败！请前往 {response.verify_url} 获取 ticket")
                raise LoginSliderNeeded(response.verify_url)
            elif response.captcha_image:
                logger.info(f"登录失败！需要根据图片输入验证码")
                raise LoginCaptchaNeeded(
                    response.captcha_image, response.captcha_sign
                )
        elif isinstance(response, AccountFrozen):
            logger.info("账号已被冻结！")
            raise LoginAccountFrozen()
        elif isinstance(response, DeviceLocked):
            self._t104 = response.t104 or self._t104
            self._t174 = response.t174 or self._t174
            self._rand_seed = response.rand_seed or self._rand_seed
            msg = "账号已开启设备锁！"
            if response.sms_phone:
                msg += f"向手机{response.sms_phone}发送验证码 "
            if response.verify_url:
                msg += f"或前往{response.verify_url}扫码验证"
            logger.info(msg + ". " + str(response.message))
            raise LoginDeviceLocked(
                response.sms_phone, response.verify_url, response.message
            )
        elif isinstance(response, TooManySMSRequest):
            logger.info("验证码发送频繁！")
            raise LoginSMSRequestError()
        elif isinstance(response, DeviceLockLogin):
            self._t104 = response.t104 or self._t104
            self._rand_seed = response.rand_seed or self._rand_seed
            # TODO: send device login packet
            pass
        elif isinstance(response, UnknownLoginStatus):
            t146 = response._tlv_map.get(0x146)
            t149 = response._tlv_map.get(0x149)
            if t146:
                packet = Packet(t146)
                msg = packet.read_bytes(packet.read_uint16(4), 6).decode()
            elif t149:
                packet = Packet(t149)
                msg = packet.read_bytes(packet.read_uint16(2), 4).decode()
            else:
                msg = ""
            logger.info(f"未知的登录返回码 {response.status}! {msg}")
            raise LoginException(response.status)
        return response
