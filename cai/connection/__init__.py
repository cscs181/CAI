"""Low Level Async TCP Connection

This module is used to build a async TCP connection to target.

Copyright (C) 2021-2021  yanyongyu

License AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import asyncio
from typing import Any, Optional

from cai.utils.coroutine import _ContextManager


class Connection:

    def __init__(
        self,
        host: str,
        port: int,
        ssl: bool = False,
        timeout: Optional[float] = None
    ) -> None:
        self._host = host
        self._port = port
        self._ssl = ssl
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
    def closed(self) -> bool:
        return self._writer is None

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return

    async def _connect(self):
        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self._host, self._port, ssl=self._ssl),
                self.timeout
            )
        except Exception as e:
            if self._writer:
                self._writer.transport.close()
            self._reader = None
            self._writer = None
            raise ConnectionError(
                f"Open connection to {self._host}:{self._port} failed"
            ) from e

    async def close(self):
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()
        self._writer = None
        self._reader = None

    async def _read_bytes(self, num_bytes: int):
        try:
            data = await self._reader.readexactly(num_bytes)
        except (asyncio.IncompleteReadError, IOError, OSError) as e:
            raise ConnectionAbortedError(
                f"Lost connection to {self._host}:{self._port}"
            ) from e
        return data

    async def _read_line(self):
        try:
            data = await self._reader.readline()
        except (asyncio.IncompleteReadError, IOError, OSError) as e:
            raise ConnectionAbortedError(
                f"Lost connection to {self._host}:{self._port}"
            ) from e
        return data

    async def _read_all(self):
        try:
            data = await self._reader.read(-1)
        except (asyncio.IncompleteReadError, IOError, OSError) as e:
            raise ConnectionAbortedError(
                f"Lost connection to {self._host}:{self._port}"
            ) from e
        return data

    def _write_bytes(self, data: bytes):
        return self._writer.write(data)

    def _write_eof(self):
        if self._writer.can_write_eof():
            self._writer.write_eof()


def connect(
    host: str,
    port: int,
    ssl: bool = False,
    timeout: Optional[float] = None
) -> _ContextManager[Any, Any, Connection]:
    coro = _connect(host, port, ssl=ssl, timeout=timeout)
    return _ContextManager(coro)


async def _connect(*args, **kwargs):
    conn = Connection(*args, **kwargs)
    await conn._connect()
    return conn
