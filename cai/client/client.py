"""Application Client Class.

This module is used to control client actions (low-level api).

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import time
import struct
import secrets
import asyncio
from typing import Any, List, Dict, Union, Optional, Callable, Awaitable

from .sso_server import get_sso_server, SsoServer
from .wtlogin import (
    encode_login_request2_captcha,
    encode_login_request2_slider,
    encode_login_request7,
    encode_login_request8,
    encode_login_request9,
    encode_login_request20,
    encode_exchange_emp_15,
    handle_oicq_response,
    OICQResponse,
    LoginSuccess,
    NeedCaptcha,
    AccountFrozen,
    DeviceLocked,
    TooManySMSRequest,
    DeviceLockLogin,
    UnknownLoginStatus,
)
from .status_service import (
    encode_register,
    handle_register_response,
    OnlineStatus,
    RegPushReason,
    SvcRegisterResponse,
    RegisterSuccess,
    RegisterFail,
)
from .friendlist import (
    encode_get_friend_list,
    handle_friend_list,
    encode_get_troop_list,
    handle_troop_list,
    FriendListEvent,
    FriendListSuccess,
    FriendListFail,
    TroopListEvent,
    TroopListSuccess,
    TroopListFail,
    StTroopNum,
)
from .heartbeat import encode_heartbeat, handle_heartbeat, Heartbeat
from .config_push import handle_config_push_request, FileServerPushList

from cai.exceptions import (
    ApiResponseError,
    LoginException,
    LoginSliderNeeded,
    LoginCaptchaNeeded,
    LoginAccountFrozen,
    LoginDeviceLocked,
    LoginSMSRequestError,
    RegisterException,
    FriendListException,
    GroupListException,
)

from cai.log import logger
from .packet import IncomingPacket
from cai.utils.binary import Packet
from cai.utils.future import FutureStore
from .event import Event, _packet_to_event
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol
from cai.connection import connect, Connection
from .models import SigInfo, Friend, FriendGroup, Group

DEVICE = get_device()
APK_INFO = get_protocol()
HANDLERS: Dict[str, Callable[["Client", IncomingPacket], Awaitable[Event]]] = {
    "wtlogin.login": handle_oicq_response,
    "wtlogin.exchange_emp": handle_oicq_response,
    "StatSvc.register": handle_register_response,
    "ConfigPushSvc.PushReq": handle_config_push_request,
    "Heartbeat.Alive": handle_heartbeat,
    "friendlist.GetFriendListReq": handle_friend_list,
    "friendlist.GetTroopListReqV2": handle_troop_list,
}


class Client:
    def __init__(self, uin: int, password_md5: bytes):
        # account info
        self._uin: int = uin
        self._password_md5: bytes = password_md5
        self._nick: Optional[str] = None
        self._age: Optional[int] = None
        self._gender: Optional[int] = None
        self._status: Optional[OnlineStatus] = None
        self._friend_list: List[Friend] = []
        self._friend_group_list: List[FriendGroup] = []
        self._group_list: List[Group] = []
        self._other_clients: List[Any] = []

        # server info
        self._seq: int = 0x3635
        self._time_diff: int = 0
        self._key: bytes = secrets.token_bytes(16)
        self._session_id: bytes = bytes([0x02, 0xB0, 0x5B, 0x8B])
        self._connection: Optional[Connection] = None
        self._heartbeat_interval: int = 300
        self._heartbeat_enabled: bool = False
        self._file_storage_info: Optional[FileServerPushList] = None

        self._ip_address: bytes = bytes()
        self._ksid: bytes = f"|{DEVICE.imei}|A8.2.7.27f6ea96".encode()
        self._pwd_flag: bool = False
        self._rollback_sig: bytes = bytes()

        self._t104: bytes = bytes()
        self._t108: bytes = bytes()
        self._t150: bytes = bytes()
        self._t174: bytes = bytes()
        self._t402: bytes = bytes()
        self._t528: bytes = bytes()
        self._t530: bytes = bytes()

        self._siginfo: SigInfo = SigInfo()
        self._receive_store: FutureStore[int, Event] = FutureStore()

    @property
    def uin(self) -> int:
        """
        Returns:
            int: qq number of the client account.
        """
        return self._uin

    @property
    def nick(self) -> Optional[str]:
        """Only available after login.

        Returns:
            Optional[str]: nick name of the client account.
        """
        return self._nick

    @property
    def age(self) -> Optional[int]:
        """Only available after login.

        Returns:
            Optional[int]: age of the client account.
        """
        return self._age

    @property
    def gender(self) -> Optional[int]:
        """Only available after login.

        Returns:
            Optional[int]: gender of the client account.
        """
        return self._gender

    @property
    def status(self) -> Optional[OnlineStatus]:
        """See detail statuses in
        :class:`~cai.client.status_service.OnlineStatus` Enum class.

        Returns:
            Optional[OnlineStatus]: Online status of the client account.
        """
        return self._status

    @property
    def connection(self) -> Connection:
        """
        Returns:
            Connection: connection object for the client.

        Raises:
            ConnectionError: no connection available.
        """
        if not self._connection or self._connection.closed:
            raise ConnectionError(
                "Lost Connection! Use `connect` or `reconnect` first."
            )
        return self._connection

    @property
    def connected(self) -> bool:
        """
        Returns:
            bool: True if the client has connected to the server.
        """
        return bool(self._connection) and not self._connection.closed

    async def connect(self, server: Optional[SsoServer] = None) -> None:
        """Connect to the server.

        This should be called before sending any packets.

        Args:
            server (Optional[SsoServer], optional): The server you want to connect. Defaults to None.

        Raises:
            RuntimeError: Already connected to the server.
            ConnectionError: Error when connecting the server.
        """
        if self.connected:
            raise RuntimeError("Already connected to the server")

        _server = server or await get_sso_server()
        logger.info(f"Connecting to server: {_server.host}:{_server.port}")
        try:
            self._connection = await connect(
                _server.host, _server.port, ssl=False, timeout=3.0
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
        """Disconnect if already connected to the server."""
        if self._connection:
            await self._connection.close()

    async def reconnect(
        self, change_server: bool = False, server: Optional[SsoServer] = None
    ) -> None:
        """Reconnect to the server.

        The ``server`` arg only take effect if ``change_server`` is True.

        Args:
            change_server (bool, optional): True if you want to change the server. Defaults to False.
            server (Optional[SsoServer], optional): Which server you want to connect to. Defaults to None.
        """
        if not change_server and self._connection:
            await self._connection.reconnect()
            return

        exclude = (
            [self._connection.host]
            if change_server and self._connection
            else []
        )
        _server = server or await get_sso_server(
            cache=False, cache_server_list=True, exclude=exclude
        )
        await self.disconnect()
        await self.connect(_server)

    async def close(self) -> None:
        """Close the client and logout."""
        if (
            self.connected
            and self.status
            and self.status != OnlineStatus.Offline
        ):
            await self.register(OnlineStatus.Offline)
        self._receive_store.cancel_all()
        await self.disconnect()

    @property
    def seq(self) -> int:
        """
        Returns:
            int: current packet sequence number.
        """
        return self._seq

    def next_seq(self) -> int:
        """Get next packet sequence number.

        Returns:
            int: next sequence number.
        """
        self._seq = (self._seq + 1) % 0x7FFF
        return self._seq

    async def send(
        self, seq: int, command_name: str, packet: Union[bytes, Packet]
    ) -> None:
        """Send a packet with the given sequence but not wait for the response.

        Args:
            seq (int): Sequence number.
            command_name (str): Command name of the packet.
            packet (Union[bytes, Packet]): Packet to send.

        Returns:
            None.
        """
        logger.debug(f"--> {seq}: {command_name}")
        await self.connection.awrite(packet)

    async def send_and_wait(
        self,
        seq: int,
        command_name: str,
        packet: Union[bytes, Packet],
        timeout: Optional[float] = 10.0,
    ) -> Event:
        """Send a packet with the given sequence and wait for the response.

        Args:
            seq (int): Sequence number.
            command_name (str): Command name of the packet.
            packet (Union[bytes, Packet]): Packet to send.
            timeout (Optional[float], optional): Timeout. Defaults to 10.

        Returns:
            Event: Response.
        """
        await self.send(seq, command_name, packet)
        return await self._receive_store.fetch(seq, timeout)

    async def receive(self):
        """Receive data from connection reader and store it in sequence future.

        Note:
            Source: com.tencent.mobileqq.msf.core.auth.n.a
        """
        while self.connected:
            try:
                length: int = (
                    struct.unpack(">i", await self.connection.read_bytes(4))[0]
                    - 4
                )
                # FIXME: length < 0 ?
                data = await self.connection.read_bytes(length)
                packet = IncomingPacket.parse(
                    data,
                    self._key,
                    self._siginfo.d2key,
                    self._siginfo.wt_session_ticket_key,
                )
                logger.debug(
                    f"<-- {packet.seq} ({packet.ret_code}): {packet.command_name}"
                )
                handler = HANDLERS.get(packet.command_name, _packet_to_event)
                packet = await handler(self, packet)
                self._receive_store.store_result(packet.seq, packet)
                # TODO: broadcast packet
            except ConnectionAbortedError:
                logger.debug("Connection closed")
            except Exception as e:
                # TODO: handle exception
                logger.exception(e)

    async def _handle_login_response(
        self, response: Event, try_times: int = 1
    ) -> LoginSuccess:
        if not isinstance(response, OICQResponse):
            raise RuntimeError("Invalid login response type!")

        if not isinstance(response, UnknownLoginStatus):
            raise ApiResponseError(
                response.uin,
                response.seq,
                response.ret_code,
                response.command_name,
            )

        if isinstance(response, LoginSuccess):
            logger.info(f"{self.nick}({self.uin}) 登录成功！")
            return response
        elif isinstance(response, NeedCaptcha):
            if response.verify_url:
                logger.info(f"登录失败！请前往 {response.verify_url} 获取 ticket")
                raise LoginSliderNeeded(response.uin, response.verify_url)
            elif response.captcha_image:
                logger.info(f"登录失败！需要根据图片输入验证码")
                raise LoginCaptchaNeeded(
                    response.uin, response.captcha_image, response.captcha_sign
                )
            else:
                raise LoginException(
                    response.uin,
                    response.status,
                    "Cannot get verify_url or captcha_image from the response!",
                )
        elif isinstance(response, AccountFrozen):
            logger.info("账号已被冻结！")
            raise LoginAccountFrozen(response.uin)
        elif isinstance(response, DeviceLocked):
            msg = "账号已开启设备锁！"
            if response.sms_phone:
                msg += f"向手机{response.sms_phone}发送验证码 "
            if response.verify_url:
                msg += f"或前往{response.verify_url}扫码验证"
            logger.info(msg + ". " + str(response.message))

            raise LoginDeviceLocked(
                response.uin,
                response.sms_phone,
                response.verify_url,
                response.message,
            )
        elif isinstance(response, TooManySMSRequest):
            logger.info("验证码发送频繁！")
            raise LoginSMSRequestError(response.uin)
        elif isinstance(response, DeviceLockLogin):
            if try_times:
                seq = self.next_seq()
                packet = encode_login_request20(
                    seq,
                    self._key,
                    self._session_id,
                    self._ksid,
                    self.uin,
                    self._t104,
                    self._siginfo.g,
                )
                response = await self.send_and_wait(
                    seq, "wtlogin.login", packet
                )
                return await self._handle_login_response(
                    response, try_times - 1
                )
            else:
                raise LoginException(
                    response.uin,
                    response.status,
                    "Maximum number of login attempts exceeded!",
                )
        elif isinstance(response, UnknownLoginStatus):
            t146 = response._tlv_map.get(0x146)
            t149 = response._tlv_map.get(0x149)
            if t146:
                packet_ = Packet(t146)
                msg = packet_.start(4).string(2).execute()[0]
            elif t149:
                packet_ = Packet(t149)
                msg = packet_.start(2).string(2).execute()[0]
            else:
                msg = ""
            logger.info(f"未知的登录返回码 {response.status}! {msg}")
            raise LoginException(
                response.uin, response.status, "Unknown login status."
            )

    async def login(self) -> LoginSuccess:
        """Login the account of the client.

        This should be called before using any other apis.

        Returns:
            LoginSuccess: Success login event.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Invalid response got. Like unknown return code.
            LoginSliderNeeded: Slider ticket needed.
            LoginCaptchaNeeded: Captcha image needed.
            LoginAccountFrozen: Account is frozen.
            LoginDeviceLocked: Device lock detected.
            LoginSMSRequestError: Too many SMS messages were sent.
            LoginException: Unknown login return code or other exception.
        """
        seq = self.next_seq()
        packet = encode_login_request9(
            seq,
            self._key,
            self._session_id,
            self._ksid,
            self.uin,
            self._password_md5,
        )
        response = await self.send_and_wait(seq, "wtlogin.login", packet)
        return await self._handle_login_response(response)

    async def submit_captcha(
        self, captcha: str, captcha_sign: bytes
    ) -> LoginSuccess:
        """Submit captcha when login captcha needed.

        This should be called after :class:`~cai.exceptions.LoginCaptchaNeeded` occurred.

        Returns:
            LoginSuccess: Success login event.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Invalid response got. Like unknown return code.
            LoginSliderNeeded: Slider ticket needed.
            LoginCaptchaNeeded: Captcha image needed.
            LoginAccountFrozen: Account is frozen.
            LoginDeviceLocked: Device lock detected.
            LoginSMSRequestError: Too many SMS messages were sent.
            LoginException: Unknown login return code or other exception.
        """
        seq = self.next_seq()
        packet = encode_login_request2_captcha(
            seq,
            self._key,
            self._session_id,
            self._ksid,
            self.uin,
            captcha,
            captcha_sign,
            self._t104,
        )
        response = await self.send_and_wait(seq, "wtlogin.login", packet)
        return await self._handle_login_response(response)

    async def submit_slider_ticket(self, ticket: str) -> LoginSuccess:
        """Submit slider ticket when login slider captcha needed.

        This should be called after :class:`~cai.exceptions.LoginSliderNeeded` occurred.

        Returns:
            LoginSuccess: Success login event.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Invalid response got. Like unknown return code.
            LoginSliderNeeded: Slider ticket needed.
            LoginCaptchaNeeded: Captcha image needed.
            LoginAccountFrozen: Account is frozen.
            LoginDeviceLocked: Device lock detected.
            LoginSMSRequestError: Too many SMS messages were sent.
            LoginException: Unknown login return code or other exception.
        """
        seq = self.next_seq()
        packet = encode_login_request2_slider(
            seq,
            self._key,
            self._session_id,
            self._ksid,
            self.uin,
            ticket,
            self._t104,
        )
        response = await self.send_and_wait(seq, "wtlogin.login", packet)
        return await self._handle_login_response(response)

    async def request_sms(self) -> bool:
        """Request new sms message when login sms code needed.

        This should be called after :class:`~cai.exceptions.LoginSMSRequestError` occurred.

        Returns:
            LoginSuccess: Success login event.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Invalid response got. Like unknown return code.
            LoginSliderNeeded: Slider ticket needed.
            LoginCaptchaNeeded: Captcha image needed.
            LoginAccountFrozen: Account is frozen.
            LoginDeviceLocked: Device lock detected.
            LoginSMSRequestError: Too many SMS messages were sent.
            LoginException: Unknown login return code or other exception.
        """
        seq = self.next_seq()
        packet = encode_login_request8(
            seq,
            self._key,
            self._session_id,
            self._ksid,
            self.uin,
            self._t104,
            self._t174,
        )
        response = await self.send_and_wait(seq, "wtlogin.login", packet)

        try:
            await self._handle_login_response(response)
            return True
        except LoginDeviceLocked:
            return True
        except Exception:
            raise

    async def submit_sms(self, sms_code: str) -> LoginSuccess:
        """Submit sms code when login sms code needed.

        This should be called after :class:`~cai.exceptions.LoginSMSRequestError` occurred.

        Returns:
            LoginSuccess: Success login event.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Invalid response got. Like unknown return code.
            LoginSliderNeeded: Slider ticket needed.
            LoginCaptchaNeeded: Captcha image needed.
            LoginAccountFrozen: Account is frozen.
            LoginDeviceLocked: Device lock detected.
            LoginSMSRequestError: Too many SMS messages were sent.
            LoginException: Unknown login return code or other exception.
        """
        seq = self.next_seq()
        packet = encode_login_request7(
            seq,
            self._key,
            self._session_id,
            self._ksid,
            self.uin,
            sms_code,
            self._t104,
            self._t174,
            self._siginfo.g,
        )
        response = await self.send_and_wait(seq, "wtlogin.login", packet)
        return await self._handle_login_response(response)

    async def _get_s_key(self) -> bytes:
        if time.time() > self._siginfo.s_key_expire_time:
            await self.refresh_siginfo()
        return self._siginfo.s_key

    async def _handle_refresh_response(
        self, response: Event, try_times: int = 1
    ) -> LoginSuccess:
        if not isinstance(response, OICQResponse):
            raise RuntimeError("Invalid refresh siginfo response type!")

        if not isinstance(response, UnknownLoginStatus):
            raise ApiResponseError(
                response.uin,
                response.seq,
                response.ret_code,
                response.command_name,
            )

        if isinstance(response, LoginSuccess):
            return response
        elif isinstance(response, AccountFrozen):
            raise LoginAccountFrozen(response.uin)
        elif isinstance(response, DeviceLockLogin):
            if try_times:
                seq = self.next_seq()
                packet = encode_login_request20(
                    seq,
                    self._key,
                    self._session_id,
                    self._ksid,
                    self.uin,
                    self._t104,
                    self._siginfo.g,
                )
                response = await self.send_and_wait(
                    seq, "wtlogin.login", packet
                )
                return await self._handle_refresh_response(
                    response, try_times - 1
                )
            else:
                raise LoginException(
                    response.uin,
                    response.status,
                    "Maximum number of login attempts exceeded!",
                )
        elif isinstance(response, UnknownLoginStatus):
            raise LoginException(
                response.uin,
                response.status,
                "Refresh siginfo received wrong response type!",
            )

    async def refresh_siginfo(self) -> LoginSuccess:
        """Submit sms code when login sms code needed.

        This should be called after :class:`~cai.exceptions.LoginSMSRequestError` occurred.

        Returns:
            LoginSuccess: Success login event.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Refresh siginfo failed.
            LoginAccountFrozen: Account is frozen.
            LoginException: Unknown login return code or other exception.
        """
        seq = self.next_seq()
        packet = encode_exchange_emp_15(
            seq,
            self._session_id,
            self.uin,
            self._siginfo.g,
            self._siginfo.dpwd,
            self._siginfo.no_pic_sig,
            self._siginfo.encrypted_a1,
            self._siginfo.rand_seed,
            self._siginfo.wt_session_ticket,
            self._siginfo.wt_session_ticket_key,
        )
        response = await self.send_and_wait(seq, "wtlogin.exchange_emp", packet)

        return await self._handle_refresh_response(response)

    async def register(
        self,
        status: OnlineStatus = OnlineStatus.Online,
        register_reason: RegPushReason = RegPushReason.AppRegister,
        battery_status: Optional[int] = None,
        is_power_connected: bool = False,
    ) -> RegisterSuccess:
        """Register app client and get login status.

        This should be called after :meth:`.Client.login` successed.

        Args:
            status (OnlineStatus, optional): Client status. Defaults to
                :attr:`~cai.client.status_service.OnlineStatus.Online`.
            register_reason (RegPushReason, optional): Register reason. Defaults to
                :attr:`~cai.client.status_service.RegPushReason.AppRegister`.
            battery_status (Optional[int], optional): Battery capacity. Defaults to ``None``.
            is_power_connected (bool, optional): Is power connected to phone. Defaults to ``False``.

        Returns:
            RegisterSuccess: Register success response.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Register failed.
        """
        seq = self.next_seq()
        packet = encode_register(
            seq,
            self._session_id,
            self._ksid,
            self.uin,
            self._siginfo.tgt,
            self._siginfo.d2,
            self._siginfo.d2key,
            7 if status == OnlineStatus.Online else 0,
            status,
            register_reason,
            battery_status,
            is_power_connected,
        )
        response = await self.send_and_wait(seq, "StatSvc.register", packet)

        if not isinstance(response, SvcRegisterResponse):
            raise RuntimeError("Invalid register response type!")

        if isinstance(response, RegisterFail):
            raise RegisterException(
                response.uin, response.ret_code, response.message or ""
            )
        elif isinstance(response, RegisterSuccess):
            asyncio.create_task(self.heartbeat())
            return response

        raise ApiResponseError(
            response.uin, response.seq, response.ret_code, response.command_name
        )

    async def heartbeat(self) -> None:
        """Do heartbeat.

        Calling this method more than once takes no effect.

        Heartbeat will be down when an error occurred.

        Example:
            Create a heartbeat task using ``asyncio``.

            >>> import asyncio
            >>> asyncio.create_task(client.heartbeat())
        """
        if self._heartbeat_enabled:
            return

        self._heartbeat_enabled = True

        while self._heartbeat_enabled and self.connected:
            seq = self.next_seq()
            packet = encode_heartbeat(
                seq, self._session_id, self._ksid, self.uin
            )
            try:
                response = await self.send_and_wait(
                    seq, "Heartbeat.Alive", packet
                )
                if not isinstance(response, Heartbeat):
                    raise RuntimeError("Invalid heartbeat response type!")
            except Exception:
                logger.exception("Heartbeat.Alive: Failed")
                break
            await asyncio.sleep(self._heartbeat_interval)

        self._heartbeat_enabled = False

    async def _refresh_friend_list(self):
        friend_count = 0xFFFFFFFF_FFFFFFFF
        group_count = 0xFFFFFFFF_FFFFFFFF
        friend_list: List[Friend] = []
        group_list: List[FriendGroup] = []
        while len(friend_list) < friend_count or len(group_list) < group_count:
            seq = self.next_seq()
            packet = encode_get_friend_list(
                seq,
                self._session_id,
                self.uin,
                self._siginfo.d2key,
                len(friend_list),
                200 if len(friend_list) < friend_count else 0,
                len(group_list),
                100 if len(group_list) < group_count else 0,
            )
            response = await self.send_and_wait(
                seq, "friendlist.GetFriendListReq", packet
            )

            if not isinstance(response, FriendListEvent):
                raise RuntimeError("Invalid get friend list response type!")
            if isinstance(response, FriendListSuccess):
                friend_list.extend(
                    map(
                        lambda x: Friend.from_dict(x.dict()),
                        response.response.friend_info,
                    )
                )
                group_list.extend(
                    map(
                        lambda x: FriendGroup.from_dict(x.dict()),
                        response.response.group_info,
                    )
                )
                friend_count = response.response.total_friend_count
                group_count = response.response.total_group_count
                continue
            elif isinstance(response, FriendListFail):
                raise FriendListException(
                    response.uin, response.result, response.message
                )
            raise ApiResponseError(
                response.uin,
                response.seq,
                response.ret_code,
                response.command_name,
            )
        self._friend_list = friend_list
        self._friend_group_list = group_list

    async def get_friend_list(self, cache: bool = True) -> List[Friend]:
        """Get Friend List.

        Return cached friend list if cache is ``True``.

        Args:
            cache (bool, optional): Use cached friend list. Defaults to True.

        Returns:
            List of :obj:`~cai.client.models.Friend`

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend list failed.
            FriendListException: Get friend list returned non-zero ret code.
        """
        if cache and self._friend_list:
            return self._friend_list

        await self._refresh_friend_list()
        return self._friend_list

    async def get_friend_group_list(
        self, cache: bool = True
    ) -> List[FriendGroup]:
        """Get Friend Group List.

        Return cached friend list if cache is ``True``.

        Args:
            cache (bool, optional): Use cached friend group list. Defaults to True.

        Returns:
            List of :obj:`~cai.client.models.FriendGroup`

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend group list failed.
            FriendListException: Get friend group list returned non-zero ret code.
        """
        if cache and self._friend_group_list:
            return self._friend_group_list

        await self._refresh_friend_list()
        return self._friend_group_list

    async def _handle_group_list_response(
        self, response: Event, try_times: int = 1
    ) -> List[Group]:
        if not isinstance(response, TroopListEvent):
            raise RuntimeError("Invalid get group list response type!")

        group_list: List[Group] = []
        if isinstance(response, TroopListSuccess):
            group_list.extend(
                map(
                    lambda x: Group.from_dict(x.dict()),
                    response.response.troop_list,
                )
            )
            if response.response.cookies and try_times:
                seq = self.next_seq()
                packet = encode_get_troop_list(
                    seq,
                    self._session_id,
                    self.uin,
                    self._siginfo.d2key,
                    cookies=response.response.cookies,
                )
                response = await self.send_and_wait(
                    seq, "friendlist.GetTroopListReqV2", packet
                )
                group_list.extend(
                    await self._handle_group_list_response(
                        response, try_times - 1
                    )
                )
            self._group_list = group_list
            return group_list
        elif isinstance(response, TroopListFail):
            raise GroupListException(
                response.uin, response.result, response.message
            )

        raise ApiResponseError(
            response.uin,
            response.seq,
            response.ret_code,
            response.command_name,
        )

    async def get_group_list(self, cache: bool = True) -> List[Group]:
        """Get Group List.

        Return cached group list if cache is ``True``.

        Args:
            cache (bool, optional): Use cached group list. Defaults to True.

        Returns:
            List of :obj:`~cai.client.models.Group`

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get group list failed.
            GroupListException: Get group list returned non-zero ret code.
        """
        if cache and self._group_list:
            return self._group_list

        seq = self.next_seq()
        packet = encode_get_troop_list(
            seq, self._session_id, self.uin, self._siginfo.d2key
        )
        response = await self.send_and_wait(
            seq, "friendlist.GetTroopListReqV2", packet
        )
        return await self._handle_group_list_response(response)
