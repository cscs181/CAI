"""Application Client Class.

This module is used to control client actions.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
from typing import Optional

from cai.settings.device import get_device
from cai.settings.protocol import get_protocol
from cai.connection import connect, Connection
from .sso_server import get_sso_server, SsoServer

DEVICE = get_device()
APK_INFO = get_protocol()


class Client:

    def __init__(self):
        self._connection: Optional[Connection] = None

    @property
    def connection(self) -> Connection:
        if not self._connection:
            raise ConnectionError("Lost Connection")
        return self._connection

    async def connect(self, server: Optional[SsoServer] = None) -> None:
        _server = server or await get_sso_server()
        try:
            self._connection = await connect(
                _server.host, _server.port, ssl=True, timeout=3.
            )
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
