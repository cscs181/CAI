import time
import logging
import unittest
from types import TracebackType
from typing import Any, Type, Tuple, Union, Optional

from cai.log import logger
from cai.connection import connect, Connection

_SysExcInfoType = Union[Tuple[Type[BaseException], BaseException,
                              Optional[TracebackType]], Tuple[None, None, None]]


class TestConnection(unittest.IsolatedAsyncioTestCase):

    def log(
        self,
        level: int,
        message: str,
        *args: Any,
        exc_info: Union[None, bool, Exception, _SysExcInfoType] = False,
        **kwargs: Any
    ):
        message = "| TestConnection | " + message
        return logger.log(level, message, *args, exc_info=exc_info, **kwargs)

    def setUp(self):
        self.log(logging.INFO, "Start Testing Connection...")

    def tearDown(self):
        self.log(logging.INFO, "End Testing Connection!")

    async def test_tcp_echo(self):
        MSG: bytes = b"Hello"

        self.log(logging.INFO, "test tcp echo")

        start = time.time()
        conn = await connect("tcpbin.com", 4242, timeout=10.)
        end = time.time()
        self.assertIsInstance(conn, Connection)
        self.log(logging.INFO, f"connected in {end - start} seconds")

        conn.write_bytes(MSG)
        conn.write_eof()
        resp = await conn.read_all()
        self.log(logging.INFO, f"received in {time.time() - end} seconds")
        await conn.close()
        self.assertEqual(resp, MSG)

        self.log(logging.INFO, "test tcp echo with context manager")

        start = time.time()
        async with connect("tcpbin.com", 4242, timeout=10.) as conn:
            end = time.time()
            self.log(logging.INFO, f"connected in {end - start} seconds")

            conn.write_bytes(MSG)
            conn.write_eof()
            resp = await conn.read_all()
            self.log(logging.INFO, f"received in {time.time() - end} seconds")
            self.assertEqual(resp, MSG)


if __name__ == "__main__":
    unittest.main()
