"""Application Client APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

import hashlib
from typing import Union, Optional

from .login import Login as _Login
from .friend import Friend as _Friend
from .group import Group as _Group
from cai.client import OnlineStatus, Client as client_t


def make_client(uin: int, passwd: Union[str, bytes]) -> client_t:
    if not (isinstance(passwd, bytes) and len(passwd) == 16):
        # not a vailed md5 passwd
        if isinstance(passwd, bytes):
            passwd = hashlib.md5(passwd).digest()
        else:
            passwd = hashlib.md5(passwd.encode()).digest()
    return client_t(uin, passwd)


class Client(_Login, _Friend, _Group):
    def __init__(self, client: client_t):
        self.client = client

    @property
    def connected(self) -> bool:
        return self.client.connected

    async def close(self):
        """Stop Client"""
        await self.client.close()

    async def set_status(
        self,
        status: Union[int, OnlineStatus],
        battery_status: Optional[int] = None,
        is_power_connected: bool = False
    ) -> None:
        """Change client status.

        This function wraps the :meth:`~cai.client.client.Client.register`
        method of the client.

        Args:
            status (OnlineStatus): Status want to change.
            battery_status (Optional[int], optional): Battery capacity.
                Defaults to None.
            is_power_connected (bool, optional): Is power connected to phone.
                Defaults to False.
            uin (Optional[int], optional): Account of the client want to change.
                Defaults to None.

        Raises:
            RuntimeError: Client already exists and is running.
            RuntimeError: Password not provided when login a new account.
            ApiResponseError: Invalid API request.
            RegisterException: Register Failed.
        """
        await self.client.set_status(
            status,
            battery_status,
            is_power_connected,
        )


__all__ = ["Client"]
