"""Application Client Class.

This module is used to control client actions.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import struct
import secrets
import asyncio
from typing import Any, List, Dict, Union, Optional, Callable

from .login import encode_login_request, decode_login_response, OICQResponse

from cai.log import logger
from .siginfo import SigInfo
from .packet import IncomingPacket
from cai.utils.binary import Packet
from cai.utils.future import FutureStore
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol
from cai.connection import connect, Connection
from .sso_server import get_sso_server, SsoServer

DEVICE = get_device()
APK_INFO = get_protocol()
HANDLERS: Dict[str, Callable[[IncomingPacket], IncomingPacket]] = {
    "wtlogin.login": decode_login_response
}


class Client:

    def __init__(self, uin: int, password_md5: bytes):
        # account info
        self._uin: int = uin
        self._password_md5: bytes = password_md5
        self._age: Optional[int] = None
        self._gender: Optional[int] = None
        # TODO
        self._friend_list: List[Any] = []
        self._group_list: List[Any] = []
        self._other_clients: List[Any] = []

        self._seq: int = 0x3635
        self._key: bytes = secrets.token_bytes(16)
        self._siginfo: SigInfo = SigInfo()
        self._session_id: bytes = bytes([0x02, 0xB0, 0x5B, 0x8B])
        self._connection: Optional[Connection] = None
        self._receive_store: FutureStore[int, IncomingPacket] = FutureStore()

    @property
    def uin(self) -> int:
        return self._uin

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
        return not self._connection.closed

    async def connect(self, server: Optional[SsoServer] = None) -> None:
        if self.connected:
            raise RuntimeError("Already connected to the server")

        _server = server or await get_sso_server()
        try:
            self._connection = await connect(
                _server.host, _server.port, ssl=True, timeout=3.
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
        timeout: Optional[float] = None
    ) -> IncomingPacket:
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
                logger.debug(f"<-- {packet.seq}: {packet.command_name}")
                handler = HANDLERS.get(packet.command_name)
                if handler:
                    packet = handler(packet)
                self._receive_store.store_result(packet.seq, packet)
                # TODO: broadcast packet
            except Exception as e:
                # TODO: handle exception
                pass

    async def login(self):
        seq = self.next_seq()
        packet = encode_login_request(
            seq, self._key, self._session_id, self.uin, self._password_md5
        )
        response = await self.send_and_wait(seq, "wtlogin.login", packet)
        if not isinstance(response, OICQResponse):
            raise RuntimeError("Invalid login response type!")

        # login success
        if response.status == 0:
            # TODO
            pass
        # captcha
        elif response.status == 2:
            # TODO
            pass
        elif response.status == 40:
            # TODO
            pass
        elif response.status == 160 or response.status == 239:
            # TODO
            pass
