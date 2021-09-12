"""Application Client APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

import asyncio
from typing import Union, Optional

from cai.client import Client, OnlineStatus
from cai.exceptions import ClientNotAvailable

from . import _clients


def get_client(uin: Optional[int] = None) -> Client:
    """Get the specific client or existing client.

    Args:
        uin (Optional[int], optional): Specific account client to get. Defaults to None.

    Raises:
        ClientNotAvailable: Client not exists.
        ClientNotAvailable: No client available.
        ClientNotAvailable: Multiple clients found and not specify which one to get.

    Returns:
        Client: Current client to use.
    """
    if not _clients:
        raise ClientNotAvailable(uin, f"No client available!")
    elif len(_clients) == 1 and not uin:
        return list(_clients.values())[0]
    else:
        if not uin:
            raise ClientNotAvailable(
                None, f"Multiple clients found! Specify uin to choose."
            )
        if uin not in _clients:
            raise ClientNotAvailable(None, f"Client {uin} not exists!")
        return _clients[uin]


async def close(uin: Optional[int] = None) -> None:
    """Close an existing client and delete it from clients.

    Args:
        uin (Optional[int], optional): Account of the client want to close. Defaults to None.
    """
    client = get_client(uin)
    await client.close()
    del _clients[client.uin]


async def close_all() -> None:
    """Close all existing clients and delete them."""
    tasks = [close(uin) for uin in _clients.keys()]
    await asyncio.gather(*tasks)


async def set_status(
    status: Union[int, OnlineStatus],
    battery_status: Optional[int] = None,
    is_power_connected: bool = False,
    uin: Optional[int] = None,
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
    client = get_client(uin)
    await client.set_status(
        status,
        battery_status,
        is_power_connected,
    )
