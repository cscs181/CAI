"""Application Client Class.

This module is used to control client actions (low-level api).

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import time
import struct
import asyncio
import secrets
from typing import (
    Any,
    Set,
    Dict,
    List,
    Tuple,
    Union,
    Callable,
    Optional,
    Awaitable,
    overload,
)

from cachetools import TTLCache

from cai import log
from cai.utils.binary import Packet
from cai.client.events.base import Event
from cai.utils.future import FutureStore
from cai.settings.protocol import ApkInfo
from cai.settings.device import DeviceInfo
from cai.connection import Connection, connect
from cai.exceptions import (
    LoginException,
    ApiResponseError,
    LoginDeviceLocked,
    LoginSliderNeeded,
    RegisterException,
    GroupListException,
    LoginAccountFrozen,
    LoginCaptchaNeeded,
    FriendListException,
    LoginSMSRequestError,
    GroupMemberListException,
)

from .packet import UniPacket, IncomingPacket
from .command import Command, _packet_to_command
from .sso_server import SsoServer, get_sso_server
from .multi_msg.long_msg import _handle_multi_resp_body
from .heartbeat import Heartbeat, encode_heartbeat, handle_heartbeat
from .models import Group, Friend, SigInfo, FriendGroup, GroupMember
from .config_push import FileServerPushList, handle_config_push_request
from .online_push import handle_c2c_sync, handle_push_msg, handle_req_push
from .message_service import (
    SyncFlag,
    GetMessageCommand,
    encode_get_message,
    handle_get_message,
    handle_push_notify,
    handle_force_offline,
)
from .status_service import (
    OnlineStatus,
    RegisterFail,
    RegPushReason,
    RegisterSuccess,
    SvcRegisterResponse,
    encode_register,
    encode_set_status,
    handle_request_offline,
    handle_register_response,
)
from .friendlist import (
    TroopListFail,
    FriendListFail,
    TroopListCommand,
    TroopListSuccess,
    FriendListCommand,
    FriendListSuccess,
    TroopMemberListFail,
    TroopMemberListCommand,
    TroopMemberListSuccess,
    handle_troop_list,
    handle_friend_list,
    encode_get_troop_list,
    encode_get_friend_list,
    handle_troop_member_list,
    encode_get_troop_member_list,
)
from .wtlogin import (
    NeedCaptcha,
    DeviceLocked,
    LoginSuccess,
    OICQResponse,
    AccountFrozen,
    DeviceLockLogin,
    TooManySMSRequest,
    UnknownLoginStatus,
    handle_oicq_response,
    encode_login_request7,
    encode_login_request8,
    encode_login_request9,
    encode_exchange_emp_15,
    encode_login_request20,
    encode_login_request2_slider,
    encode_login_request2_captcha,
)

HT = Callable[
    ["Client", IncomingPacket, Tuple[DeviceInfo, ApkInfo]], Awaitable[Command]
]
LT = Callable[["Client", Event], Awaitable[None]]

HANDLERS: Dict[str, HT] = {
    "wtlogin.login": handle_oicq_response,
    "wtlogin.exchange_emp": handle_oicq_response,
    "StatSvc.register": handle_register_response,
    "StatSvc.SetStatusFromClient": handle_register_response,
    "StatSvc.ReqMSFOffline": handle_request_offline,
    "ConfigPushSvc.PushReq": handle_config_push_request,
    "Heartbeat.Alive": handle_heartbeat,
    "friendlist.GetFriendListReq": handle_friend_list,
    "friendlist.GetTroopListReqV2": handle_troop_list,
    "friendlist.GetTroopMemberListReq": handle_troop_member_list,
    "MessageSvc.PbGetMsg": handle_get_message,
    "MessageSvc.PushNotify": handle_push_notify,
    "MessageSvc.PushForceOffline": handle_force_offline,
    "OnlinePush.PbPushGroupMsg": handle_push_msg,
    "OnlinePush.PbPushDisMsg": handle_push_msg,
    "OnlinePush.PbC2CMsgSync": handle_c2c_sync,
    "OnlinePush.PbPushC2CMsg": handle_push_msg,
    # "OnlinePush.PbPushBindUinGroupMsg": handle_push_msg,  # sub account
    # new
    "MultiMsg.ApplyUp": _handle_multi_resp_body,
    "OnlinePush.ReqPush": handle_req_push,
}


class Client:
    LISTENERS: Set[LT] = set()

    def __init__(
        self,
        uin: int,
        password_md5: bytes,
        device: DeviceInfo,
        apk_info: ApkInfo,
        *,
        auto_reconnect: bool = True,
        max_reconnections: Optional[int] = 3,
    ):
        # client info
        self._device: DeviceInfo = device
        self._apk_info: ApkInfo = apk_info

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
        self._ksid: bytes = f"|{device.imei}|A8.2.7.27f6ea96".encode()
        self._pwd_flag: bool = False
        self._rollback_sig: bytes = bytes()

        self._t104: bytes = bytes()
        self._t108: bytes = bytes()
        self._t150: bytes = bytes()
        self._t174: bytes = bytes()
        self._t402: bytes = bytes()
        self._t528: bytes = bytes()
        self._t530: bytes = bytes()

        self._init_flag: bool = False
        self._listeners: Set[LT] = set()
        self._siginfo: SigInfo = SigInfo()
        self._sync_cookie: bytes = bytes()
        self._pubaccount_cookie: bytes = bytes()
        self._msg_cache: TTLCache = TTLCache(maxsize=1024, ttl=3600)
        self._receive_store: FutureStore[int, Command] = FutureStore()

        # connection info
        self._reconnect: bool = auto_reconnect
        self._reconnect_times: int = 0
        self._max_reconnections: Optional[int] = max_reconnections
        self._closed: asyncio.Event = asyncio.Event()

    def __str__(self) -> str:
        return f"<cai client object {self.uin}(connected={self.connected})>"

    @property
    def device(self) -> DeviceInfo:
        """
        Returns:
            DeviceInfo: client device info
        """
        return self._device

    @property
    def apk_info(self) -> ApkInfo:
        """
        Returns:
            ApkInfo: client apk(protocol) info
        """
        return self._apk_info

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
        return bool(self._connection and not self._connection.closed)

    @property
    def closed(self) -> bool:
        return self._closed.is_set()

    async def wait_closed(self):
        await self._closed.wait()

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
        if self.closed:
            raise RuntimeError("Client is closed")
        log.network.debug("Getting Sso server")
        _server = server or await get_sso_server()
        log.logger.info(f"Connecting to server: {_server.host}:{_server.port}")
        try:
            self._connection = await connect(
                _server.host, _server.port, ssl=False, timeout=3.0
            )
            task = asyncio.create_task(self.receive())
            task.add_done_callback(self._recv_done_cb)
        except ConnectionError as e:
            raise
        except Exception as e:
            raise ConnectionError(
                "An error occurred while connecting to "
                f"server({_server.host}:{_server.port}): " + repr(e)
            )

    def _recv_done_cb(self, task: asyncio.Task):
        if self._reconnect:
            if (
                self._max_reconnections
                and self._reconnect_times >= self._max_reconnections
            ):
                log.network.warning(
                    "Max reconnections reached, stop reconnecting"
                )
                asyncio.create_task(self.disconnect())
            else:
                log.network.warning("receiver stopped, try to reconnect")
                self._reconnect_times += 1
                asyncio.create_task(self.reconnect())
        else:
            log.network.warning("receiver stopped")
            asyncio.create_task(self.disconnect())

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
            log.network.warning("reconnecting...")
            await self._connection.reconnect()
            # FIXME: register reason msfByNetChange?
            await self._init(drop_offline_msg=False)
            log.network.info("reconnected")
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
        log.logger.warning("closing client")
        # disable reconnection
        self._reconnect = False
        # logout
        if (
            self.connected
            and self.status
            and self.status != OnlineStatus.Offline
        ):
            await self.register(OnlineStatus.Offline)

        # clear waiting packet
        self._receive_store.cancel_all()
        # disconnect server
        await self.disconnect()
        self._closed.set()

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
        log.network.debug(f"(send: {seq}): {command_name}")
        await self.connection.awrite(packet)

    async def send_and_wait(
        self,
        seq: int,
        command_name: str,
        packet: Union[bytes, Packet],
        timeout: Optional[float] = 10.0,
    ) -> Command:
        """Send a packet with the given sequence and wait for the response.

        Args:
            seq (int): Sequence number.
            command_name (str): Command name of the packet.
            packet (Union[bytes, Packet]): Packet to send.
            timeout (Optional[float], optional): Timeout. Defaults to 10.

        Returns:
            Command: Response.
        """
        await self.send(seq, command_name, packet)
        return await self._receive_store.fetch(seq, timeout)

    # FIXME
    async def send_unipkg_and_wait(
        self, command_name: str, enc_packet: bytes, seq=-1, timeout=10.0
    ):
        if seq == -1:
            seq = self.next_seq()
        return await self.send_and_wait(
            seq,
            command_name,
            UniPacket.build(
                self.uin,
                seq,
                command_name,
                self._session_id,
                1,
                enc_packet,
                self._siginfo.d2key,
            ),
            timeout,
        )

    async def _handle_incoming_packet(self, in_packet: IncomingPacket) -> None:
        try:
            handler = HANDLERS.get(in_packet.command_name, _packet_to_command)
            packet = await handler(
                self, in_packet, (self.device, self.apk_info)
            )
            self._receive_store.store_result(packet.seq, packet)
        except Exception as e:
            # TODO: handle exception
            log.logger.exception(e)

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
                log.network.debug(
                    f"(receive: {packet.ret_code}): {packet.command_name}"
                )
                # do not block receive
                asyncio.create_task(self._handle_incoming_packet(packet))
            except ConnectionAbortedError as e:
                log.logger.error(f"{self.uin} connection lost: {str(e)}")
                break
            except Exception as e:
                log.logger.exception(e)

    @property
    def listeners(self) -> Set[LT]:
        return self._listeners | self.LISTENERS

    async def _run_listener(self, listener: LT, event: Event) -> None:
        try:
            await listener(self, event)
        except Exception as e:
            log.logger.exception(e)

    def dispatch_event(self, event: Event) -> None:
        if event.type not in ("group_message", "private_message"):  # log filter
            log.logger.debug(f"Event {event.type} was triggered")
        for listener in self.listeners:
            asyncio.create_task(self._run_listener(listener, event))

    def add_event_listener(self, listener: LT) -> None:
        """Add event listener for this client.

        Args:
            listener (Callable[[Client, Event], Awaitable[None]]): Event listener.
        """
        self._listeners.add(listener)

    async def _handle_login_response(
        self, response: Command, try_times: int = 1
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
            log.logger.info(f"{self.nick}({self.uin}) 登录成功！")
            await self._init()
            return response
        elif isinstance(response, NeedCaptcha):
            if response.verify_url:
                log.logger.info(f"登录失败！请前往 {response.verify_url} 获取 ticket")
                raise LoginSliderNeeded(response.uin, response.verify_url)
            elif response.captcha_image:
                log.logger.info(f"登录失败！需要根据图片输入验证码")
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
            log.logger.info("账号已被冻结！")
            raise LoginAccountFrozen(response.uin)
        elif isinstance(response, DeviceLocked):
            msg = "账号已开启设备锁！"
            if response.sms_phone:
                msg += f"向手机{response.sms_phone}发送验证码"
            if response.verify_url:
                msg += f"或前往 {response.verify_url} 扫码验证"
            log.logger.info(msg + "。" + str(response.message))

            raise LoginDeviceLocked(
                response.uin,
                response.sms_phone,
                response.verify_url,
                response.message,
            )
        elif isinstance(response, TooManySMSRequest):
            log.logger.info("验证码发送过于频繁！")
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
                    self.device.imei,
                    self.apk_info,
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
            log.logger.info(f"未知的登录返回码 {response.status}! {msg}")
            raise LoginException(
                response.uin, response.status, "Unknown login status."
            )

    async def _init(self, drop_offline_msg: bool = True) -> None:
        if not self.connected or self.status == OnlineStatus.Offline:
            raise RuntimeError("Client is offline.")

        self._init_flag = drop_offline_msg

        previous_status = self._status or OnlineStatus.Online
        # register client online status
        await self.register(status=previous_status)
        # force refresh group list
        await self._refresh_group_list()
        # force refresh friend list
        await self._refresh_friend_list()
        # force refresh session message
        await self._get_message(0, online_sync_flag=1)
        self._init_flag = False

    async def login(self) -> LoginSuccess:
        """Login the account of the client.

        This should be called before using any other apis.

        Returns:
            LoginSuccess: Success login command.

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
            self.device,
            self.apk_info,
        )
        response = await self.send_and_wait(seq, "wtlogin.login", packet)
        return await self._handle_login_response(response)

    async def submit_captcha(
        self, captcha: str, captcha_sign: bytes
    ) -> LoginSuccess:
        """Submit captcha when login captcha needed.

        This should be called after :class:`~cai.exceptions.LoginCaptchaNeeded` occurred.

        Returns:
            LoginSuccess: Success login command.

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
            self.device.imei,
            self.apk_info,
        )
        response = await self.send_and_wait(seq, "wtlogin.login", packet)
        return await self._handle_login_response(response)

    async def submit_slider_ticket(self, ticket: str) -> LoginSuccess:
        """Submit slider ticket when login slider captcha needed.

        This should be called after :class:`~cai.exceptions.LoginSliderNeeded` occurred.

        Returns:
            LoginSuccess: Success login command.

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
            self.device.imei,
            self.apk_info,
        )
        response = await self.send_and_wait(seq, "wtlogin.login", packet)
        return await self._handle_login_response(response)

    async def request_sms(self) -> bool:
        """Request new sms message when login sms code needed.

        This should be called after :class:`~cai.exceptions.LoginSMSRequestError` occurred.

        Returns:
            LoginSuccess: Success login command.

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
            self.device.imei,
            self.apk_info,
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
            LoginSuccess: Success login command.

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
            self.device.imei,
            self.apk_info,
        )
        response = await self.send_and_wait(seq, "wtlogin.login", packet)
        return await self._handle_login_response(response)

    async def _get_s_key(self) -> bytes:
        if time.time() > self._siginfo.s_key_expire_time:
            await self.refresh_siginfo()
        return self._siginfo.s_key

    async def _handle_refresh_response(
        self, response: Command, try_times: int = 1
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
                    self.device.imei,
                    self.apk_info,
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
            LoginSuccess: Success login command.

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
            self.device,
            self.apk_info,
        )
        response = await self.send_and_wait(seq, "wtlogin.exchange_emp", packet)

        return await self._handle_refresh_response(response)

    async def register(
        self,
        status: OnlineStatus = OnlineStatus.Online,
        register_reason: RegPushReason = RegPushReason.AppRegister,
    ) -> RegisterSuccess:
        """Register app client and get login status.

        This should be called after :meth:`.Client.login` successed.

        Args:
            status (OnlineStatus, optional): Client status. Defaults to
                :attr:`~cai.client.status_service.OnlineStatus.Online`.
            register_reason (RegPushReason, optional): Register reason. Defaults to
                :attr:`~cai.client.status_service.RegPushReason.AppRegister`.

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
            status,
            register_reason,
            self.apk_info.sub_app_id,
            self.device,
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

    async def set_status(
        self,
        status: Union[int, OnlineStatus],
        battery_status: Optional[int] = None,
        is_power_connected: bool = False,
    ) -> RegisterSuccess:
        """Register app client and get login status.

        This should be called after :meth:`.Client.login` successed.

        Args:
            status (OnlineStatus, optional): Client status. Defaults to
                :attr:`~cai.client.status_service.OnlineStatus.Online`.
            battery_status (Optional[int], optional): Battery capacity.
                Only works when status is :obj:`.OnlineStatus.Battery`. Defaults to None.
            is_power_connected (bool, optional): Is power connected to phone.
                Only works when status is :obj:`.OnlineStatus.Battery`. Defaults to False.

        Returns:
            RegisterSuccess: Register success response.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Register failed.
        """
        seq = self.next_seq()
        packet = encode_set_status(
            seq,
            self._session_id,
            self.uin,
            self._siginfo.d2key,
            self.device,
            status,
            battery_status,
            is_power_connected,
        )
        response = await self.send_and_wait(
            seq, "StatSvc.SetStatusFromClient", packet
        )

        if not isinstance(response, SvcRegisterResponse):
            raise RuntimeError("Invalid set status response type!")

        if isinstance(response, RegisterFail):
            raise RegisterException(
                response.uin, response.ret_code, response.message or ""
            )
        elif isinstance(response, RegisterSuccess):
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

        while self._heartbeat_enabled and not self._connection.closed:
            seq = self.next_seq()
            packet = encode_heartbeat(
                seq,
                self._session_id,
                self.device.imei,
                self._ksid,
                self.uin,
                self.apk_info.sub_app_id,
            )
            try:
                response = await self.send_and_wait(
                    seq, "Heartbeat.Alive", packet
                )
                if not isinstance(response, Heartbeat):
                    raise RuntimeError("Invalid heartbeat response type!")
            except (ConnectionError, TimeoutError) as e:
                log.network.error(f"Heartbeat.Alive: failed by {str(e)}")
                break
            await asyncio.sleep(self._heartbeat_interval)

        log.network.debug("heartbeat stopped")
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

            if not isinstance(response, FriendListCommand):
                raise RuntimeError("Invalid get friend list response type!")
            if isinstance(response, FriendListSuccess):
                friend_list.extend(
                    map(
                        lambda x: Friend.from_dict(
                            {**x.dict(), "_client": self}
                        ),
                        response.response.friend_info,
                    )
                )
                group_list.extend(
                    map(
                        lambda x: FriendGroup.from_dict(
                            {**x.dict(), "_client": self}
                        ),
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

    async def get_friend(
        self, uin: int, cache: bool = True
    ) -> Optional[Friend]:
        """Get Friend.

        Return cached friend if cache is ``True``.

        Args:
            uin (int): Friend uin.
            cache (bool, optional): Use cached friend list. Defaults to True.

        Returns:
            Friend: Friend object.
            None: Friend not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend list failed.
            FriendListException: Get friend list returned non-zero ret code.
        """
        if not cache:
            await self._refresh_friend_list()

        return next(
            filter(lambda x: x.friend_uin == uin, self._friend_list), None
        )

    async def get_friend_list(self, cache: bool = True) -> List[Friend]:
        """Get Friend List.

        Return cached friend list if cache is ``True``.

        Args:
            cache (bool, optional): Use cached friend list. Defaults to True.

        Returns:
            List[Friend]: Friend list.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend list failed.
            FriendListException: Get friend list returned non-zero ret code.
        """
        if cache and self._friend_list:
            return self._friend_list

        await self._refresh_friend_list()
        return self._friend_list

    async def get_friend_group(
        self, group_id: int, cache: bool = True
    ) -> Optional[FriendGroup]:
        """Get Friend Group.

        Return cached friend group if cache is ``True``.

        Args:
            group_id (int): Friend group id.
            cache (bool, optional): Use cached friend group list. Defaults to True.

        Returns:
            FriendGroup: Friend group object.
            None: Friend group not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend group list failed.
            FriendListException: Get friend group list returned non-zero ret code.
        """
        if not cache:
            await self._refresh_friend_list()

        return next(
            filter(lambda x: x.group_id == group_id, self._friend_group_list),
            None,
        )

    async def get_friend_group_list(
        self, cache: bool = True
    ) -> List[FriendGroup]:
        """Get Friend Group List.

        Return cached friend group list if cache is ``True``.

        Args:
            cache (bool, optional): Use cached friend group list. Defaults to True.

        Returns:
            List[FriendGroup]: Friend group list.

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
        self, response: Command, try_times: int = 1
    ) -> List[Group]:
        """Handle Group List Response.

        Note:
            Source: com.tencent.mobileqq.troop.handler.TroopListHandler.a
        """
        if not isinstance(response, TroopListCommand):
            raise RuntimeError("Invalid get group list response type!")

        group_list: List[Group] = []
        if isinstance(response, TroopListSuccess):
            group_list.extend(
                map(
                    lambda x: Group.from_dict({**x.dict(), "_client": self}),
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

    async def _refresh_group_list(self):
        seq = self.next_seq()
        packet = encode_get_troop_list(
            seq, self._session_id, self.uin, self._siginfo.d2key
        )
        response = await self.send_and_wait(
            seq, "friendlist.GetTroopListReqV2", packet
        )
        group_list = await self._handle_group_list_response(response)
        self._group_list = group_list

    async def get_group(
        self, group_id: int, cache: bool = True
    ) -> Optional[Group]:
        """Get Group.

        Return cached group if cache is ``True``.

        Args:
            cache (bool, optional): Use cached group list. Defaults to True.

        Returns:
            Group: Group object.
            None: Group not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get group list failed.
            GroupListException: Get group list returned non-zero ret code.
        """
        if not cache:
            await self._refresh_group_list()

        return next(
            filter(lambda x: x.group_id == group_id, self._group_list), None
        )

    async def get_group_list(self, cache: bool = True) -> List[Group]:
        """Get Group List.

        Return cached group list if cache is ``True``.

        Args:
            cache (bool, optional): Use cached group list. Defaults to True.

        Returns:
            List[Group]: Group list.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get group list failed.
            GroupListException: Get group list returned non-zero ret code.
        """
        if cache and self._group_list:
            return self._group_list

        await self._refresh_group_list()
        return self._group_list

    async def _refresh_group_member_list(self, group: Group):
        """Handle Group Member List Response.

        Note:
            Source: com.tencent.mobileqq.troop.handler.TroopMemberListHandler.a
        """

        next_uin = 0
        has_next = True
        group_list: List[GroupMember] = []

        while has_next:
            seq = self.next_seq()
            packet = encode_get_troop_member_list(
                seq,
                self._session_id,
                self.uin,
                self._siginfo.d2key,
                group.group_uin,
                group.group_code,
                next_uin,
            )
            response = await self.send_and_wait(
                seq, "friendlist.GetTroopMemberListReq", packet
            )
            if not isinstance(response, TroopMemberListCommand):
                raise RuntimeError(
                    "Invalid get group member list response type!"
                )

            if isinstance(response, TroopMemberListSuccess):
                group_list.extend(
                    map(
                        lambda x: GroupMember.from_dict(
                            {**x.dict(), "_client": self, "_group": group}
                        ),
                        response.response.troop_member,
                    )
                )
                next_uin = response.response.next_uin
                has_next = next_uin != 0
                continue
            elif isinstance(response, TroopMemberListFail):
                raise GroupMemberListException(
                    response.uin, response.result, response.message
                )

            raise ApiResponseError(
                response.uin,
                response.seq,
                response.ret_code,
                response.command_name,
            )
        group._cached_member_list = group_list

    @overload
    async def get_group_member_list(
        self, group: int, cache: bool = True
    ) -> Optional[List[GroupMember]]:
        ...

    @overload
    async def get_group_member_list(
        self, group: Group, cache: bool = True
    ) -> List[GroupMember]:
        ...

    async def get_group_member_list(
        self, group: Union[int, Group], cache: bool = True
    ) -> Optional[List[GroupMember]]:
        """Get Group Member List.

        Return cached group member list if cache is ``True``.

        Args:
            group (Union[int, Group]): Group id or group object want to get members.
            cache (bool, optional): Use cached group list. Defaults to True.

        Returns:
            List[GroupMember]: Group member list.
            None: Group not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get group list failed.
            GroupMemberListException: Get group member list returned non-zero ret code.
        """
        if isinstance(group, int):
            group_ = await self.get_group(group, cache=True)

            if not group_:
                return
        else:
            group_ = group

        if not cache or not group_._cached_member_list:
            await self._refresh_group_member_list(group_)

        return group_._cached_member_list

    async def _get_message(
        self,
        request_type: int,
        sync_flag: SyncFlag = SyncFlag.START,
        sync_cookie: Optional[bytes] = None,
        online_sync_flag: int = 0,
        pubaccount_cookie: Optional[bytes] = None,
        server_buf: Optional[bytes] = None,
    ) -> None:
        seq = self.next_seq()
        packet = encode_get_message(
            seq,
            self._session_id,
            self.uin,
            self._siginfo.d2key,
            request_type=request_type,
            sync_flag=sync_flag,
            sync_cookie=sync_cookie,
            online_sync_flag=online_sync_flag,
            pubaccount_cookie=pubaccount_cookie,
            server_buf=server_buf,
        )
        response = await self.send_and_wait(seq, "MessageSvc.PbGetMsg", packet)

        if not isinstance(response, GetMessageCommand):
            raise RuntimeError("Invalid get message response type!")
