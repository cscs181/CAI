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
from typing import Any, List, Union, Optional

from .login import login
from cai.utils.binary import Packet
from cai.utils.future import FutureStore
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol
from cai.connection import connect, Connection
from .sso_server import get_sso_server, SsoServer

DEVICE = get_device()
APK_INFO = get_protocol()


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
        self._session_id: bytes = bytes([0x02, 0xB0, 0x5B, 0x8B])
        self._connection: Optional[Connection] = None
        self._receive_store: FutureStore[int] = FutureStore()

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

    def send(self, packet: Union[bytes, Packet]) -> None:
        self.connection.write_bytes(packet)

    async def send_and_wait(
        self,
        seq: int,
        packet: Union[bytes, Packet],
        timeout: Optional[float] = None
    ) -> bytes:
        self.send(packet)
        return await self._receive_store.fetch(seq, timeout)

    async def receive(self):
        """Receive data from connection reader and store it in sequence future.

        Note:
            Source: com.tencent.mobileqq.msf.core.auth.n.a
        """
        # TODO
        while self.connected:
            try:
                length: int = struct.unpack(
                    ">i", await self.connection.read_bytes(4)
                )[0] - 4
                # FIXME: length < 0 ?
                data = await self.connection.read_bytes(length)
            except Exception as e:
                pass

    async def login(self):
        seq = self.next_seq()
        packet = login(
            seq, self._key, self._session_id, self.uin, self._password_md5
        )
        response = await self.send_and_wait(seq, packet)
