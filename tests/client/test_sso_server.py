import logging
import unittest
import ipaddress

from cai.log import logger
from cai.client.sso_server import (
    get_sso_list,
    get_sso_server,
    SsoServer,
    SsoServerResponse,
)


class TestSsoServer(unittest.IsolatedAsyncioTestCase):
    def log(self, level: int, message: str, *args, exc_info=False, **kwargs):
        message = "| TestSsoServer | " + message
        return logger.log(level, message, *args, exc_info=exc_info, **kwargs)

    def setUp(self):
        self.log(logging.INFO, "Start Testing SsoServer...")

    def tearDown(self):
        self.log(logging.INFO, "End Testing SsoServer!")

    async def test_get_list(self):
        self.log(logging.INFO, "test get sso server response")
        sso_list = await get_sso_list()
        self.assertIsInstance(sso_list, SsoServerResponse)
        self.assertGreater(
            len(sso_list.socket_v4_mobile) + len(sso_list.socket_v4_wifi), 0
        )

    async def test_get_sso_server(self):
        self.log(logging.INFO, "test get sso server")
        sso_server = await get_sso_server(cache=False)
        self.assertIsInstance(sso_server, SsoServer)
        self.assertIsInstance(
            ipaddress.ip_address(sso_server.host), ipaddress.IPv4Address
        )

        self.log(logging.INFO, "test get sso server again with cache")
        sso_server_cached = await get_sso_server(cache=True)
        self.assertIs(sso_server_cached, sso_server)


if __name__ == "__main__":
    unittest.main()
