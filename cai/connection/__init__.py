import asyncio
from typing import Optional

from cai.utils.coroutine import _ContextManager


class Connection:

    def __init__(
        self, host: str, port: int, timeout: Optional[float] = None
    ) -> None:
        self._host = host
        self._port = port
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
    def closed(self) -> bool:
        return self._writer is None

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return

    async def _connect(self):
        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self._host, self._port), self.timeout
            )
        except Exception as e:
            if self._writer:
                self._writer.transport.close()
            self._reader = None
            self._writer = None
            raise ConnectionError(
                f"Open connection to {self._host}:{self._port} failed"
            ) from e

    def close(self):
        if self._writer:
            self._writer.transport.close()
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

    def _write_bytes(self, data: bytes):
        return self._writer.write(data)


def connect(host: str, port: int, timeout: Optional[float] = None):
    coro = _connect(host, port, timeout)
    return _ContextManager(coro)


async def _connect(*args, **kwargs):
    conn = Connection(*args, **kwargs)
    await conn._connect()
    return conn
