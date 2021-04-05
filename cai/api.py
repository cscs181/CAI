"""Application Client APIs.

This module wraps the client methods to provide easier control (high-level api).

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

import asyncio
from typing import Dict, Optional, Callable, Awaitable

from cai.log import logger
from cai.exceptions import LoginException, ClientNotAvailable
from cai.client import Client, HANDLERS, Event, IncomingPacket

_clients: Dict[int, Client] = {}


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


async def login(uin: int, password_md5: Optional[bytes] = None) -> Client:
    """Create a new client (or use an existing one) and login.

    Password md5 should be provided when login a new account.

    This function wraps the login method of the client.

    Args:
        uin (int): QQ account number.
        password_md5 (Optional[bytes], optional): md5 bytes of the password. Defaults to None.

    Raises:
        RuntimeError: Client already exists and is running.
        RuntimeError: Password not provided when login a new account.
        LoginSliderException: Need slider ticket.
        LoginCaptchaException: Need captcha image.
    """
    if uin in _clients:
        client = _clients[uin]
        if client.connected:
            raise RuntimeError(f"Client {uin} already connected!")
        client._password_md5 = password_md5 or client._password_md5
    else:
        if not password_md5:
            raise RuntimeError(f"Password md5 needed for creating new client!")
        client = Client(uin, password_md5)
        _clients[uin] = client

    await client.reconnect()
    try:
        await client.login()
        await client.register()
    except LoginException:
        raise
    except Exception:
        await client.close()
        raise
    return client


async def submit_captcha(
    captcha: str, captcha_sign: bytes, uin: Optional[int] = None
) -> bool:
    client = get_client(uin)
    try:
        await client.submit_captcha(captcha, captcha_sign)
    except LoginException:
        raise
    except Exception:
        await client.close()
        raise
    return True


async def submit_slider_ticket(ticket: str, uin: Optional[int] = None) -> bool:
    client = get_client(uin)
    try:
        await client.submit_slider_ticket(ticket)
    except LoginException:
        raise
    except Exception:
        await client.close()
        raise
    return True


async def request_sms(uin: Optional[int] = None) -> bool:
    client = get_client(uin)
    return await client.request_sms()


async def submit_sms(sms_code: str, uin: Optional[int] = None) -> bool:
    client = get_client(uin)
    try:
        await client.submit_sms(sms_code)
    except LoginException:
        raise
    except Exception:
        await client.close()
        raise
    return True


def register_packet_handler(
    cmd: str, packet_handler: Callable[[Client, IncomingPacket],
                                       Awaitable[Event]]
):
    if cmd in HANDLERS:
        logger.warning(
            f"You are overwriting an existing handler for command {cmd}!"
        )
    HANDLERS[cmd] = packet_handler


__all__ = [
    "get_client", "close", "close_all", "login", "submit_captcha",
    "submit_slider_ticket", "request_sms", "submit_sms"
]
