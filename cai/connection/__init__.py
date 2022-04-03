"""Low Level Async TCP Connection

This module is used to build a async TCP connection to target.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import asyncio
from types import TracebackType
from typing import Any, Type, Union, Optional

from cai.utils.binary import Packet
from cai.utils.coroutine import ContextManager


class Connection:
    def __init__(
        self,
        host: str,
        port: int,
        ssl: bool = False,
        timeout: Optional[float] = None,
    ) -> None:
        self._host = host
        self._port = port
        self._ssl = ssl
        self._closed = asyncio.Event()
        self.timeout = timeout

        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def ssl(self) -> bool:
        return self._ssl

    @property
    def writer(self) -> asyncio.StreamWriter:
        if not self._writer:
            raise RuntimeError("Connection closed!")
        return self._writer

    @property
    def reader(self) -> asyncio.StreamReader:
        if not self._reader:
            raise RuntimeError("Connection closed!")
        return self._reader

    @property
    def closed(self) -> bool:
        #return self._writer is None
        return self._closed.is_set()

    @property
    async def wait_closed(self):
        await self._closed.wait()

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()
        return

    async def _connect(self):
        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self._host, self._port, ssl=self._ssl),
                self.timeout,
            )
        except Exception as e:
            if self._writer:
                self._writer.transport.close()
            self._reader = None
            self._writer = None
            raise ConnectionError(
                f"Open connection to {self._host}:{self._port} failed"
            ) from e
        self._closed.clear()

    async def close(self):
        self._closed.set()
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()
        self._writer = None
        self._reader = None

    async def reconnect(self) -> None:
        await self.close()
        await self._connect()

    async def read_bytes(self, num_bytes: int):
        try:
            data = await self.reader.readexactly(num_bytes)
        except (asyncio.IncompleteReadError, IOError, OSError) as e:
            await self.close()
            raise ConnectionAbortedError(
                f"Lost connection to {self._host}:{self._port}"
            ) from e
        return data

    async def read_line(self):
        try:
            data = await self.reader.readline()
        except (asyncio.IncompleteReadError, IOError, OSError) as e:
            await self.close()
            raise ConnectionAbortedError(
                f"Lost connection to {self._host}:{self._port}"
            ) from e
        return data

    async def read_all(self):
        try:
            data = await self.reader.read(-1)
        except (asyncio.IncompleteReadError, IOError, OSError) as e:
            await self.close()
            raise ConnectionAbortedError(
                f"Lost connection to {self._host}:{self._port}"
            ) from e
        return data

    def write(self, data: Union[bytes, Packet]):
        self.writer.write(data)  # type: ignore

    def write_eof(self):
        if self.writer.can_write_eof():
            self.writer.write_eof()

    async def awrite(self, data: Union[bytes, Packet]):
        self.writer.write(data)  # type: ignore
        await self.writer.drain()


def connect(
    host: str, port: int, ssl: bool = False, timeout: Optional[float] = None
) -> ContextManager[Any, Any, Connection]:
    coro = _connect(host, port, ssl=ssl, timeout=timeout)
    return ContextManager(coro)


async def _connect(*args, **kwargs):
    conn = Connection(*args, **kwargs)
    await conn._connect()
    return conn
