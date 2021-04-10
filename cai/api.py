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
from cai.client import (
    Client,
    HANDLERS,
    Event,
    IncomingPacket,
    OnlineStatus,
    RegPushReason,
)

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

    This function wraps the :meth:`~cai.client.client.Client.login` method of the client.

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
    """Submit captcha data to login.

    This function wraps the :meth:`~cai.client.client.Client.submit_captcha`
    method of the client.

    Args:
        captcha (str): Captcha data to submit.
        captcha_sign (bytes): Captcha sign received when login.
        uin (Optional[int], optional): Account of the client want to login.
            Defaults to None.

    Raises:
        RuntimeError: Client already exists and is running.
        RuntimeError: Password not provided when login a new account.
        LoginSliderException: Need slider ticket.
        LoginCaptchaException: Need captcha image.
    """
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
    """Submit slider ticket to login.

    This function wraps the :meth:`~cai.client.client.Client.submit_slider_ticket`
    method of the client.

    Args:
        ticket (str): Slider ticket to submit.
        uin (Optional[int], optional): Account of the client want to login.
            Defaults to None.

    Raises:
        RuntimeError: Client already exists and is running.
        RuntimeError: Password not provided when login a new account.
        LoginSliderException: Need slider ticket.
        LoginCaptchaException: Need captcha image.
    """
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
    """Request sms code message to login.

    This function wraps the :meth:`~cai.client.client.Client.request_sms`
    method of the client.

    Args:
        uin (Optional[int], optional): Account of the client want to login.
            Defaults to None.

    Raises:
        RuntimeError: Client already exists and is running.
        RuntimeError: Password not provided when login a new account.
        LoginSMSRequestError: Too many SMS messages were sent.
    """
    client = get_client(uin)
    return await client.request_sms()


async def submit_sms(sms_code: str, uin: Optional[int] = None) -> bool:
    """Submit sms code to login.

    This function wraps the :meth:`~cai.client.client.Client.submit_sms`
    method of the client.

    Args:
        sms_code (str): SMS code to submit.
        uin (Optional[int], optional): Account of the client want to login.
            Defaults to None.

    Raises:
        RuntimeError: Client already exists and is running.
        RuntimeError: Password not provided when login a new account.
        LoginSliderException: Need slider ticket.
        LoginCaptchaException: Need captcha image.
    """
    client = get_client(uin)
    try:
        await client.submit_sms(sms_code)
    except LoginException:
        raise
    except Exception:
        await client.close()
        raise
    return True


async def set_status(
    status: OnlineStatus,
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
    await client.register(
        status,
        RegPushReason.SetOnlineStatus,
        battery_status,
        is_power_connected,
    )


def register_packet_handler(
    cmd: str,
    packet_handler: Callable[[Client, IncomingPacket], Awaitable[Event]],
) -> None:
    """Register custom packet handler.

    Note:
        This function is a low-level api to mock default behavior. Be aware of what you are doing!

    Args:
        cmd (str): Command name of the packet.
        packet_handler (Callable[[Client, IncomingPacket], Awaitable[Event]]):
            Asynchronous packet handler. A :obj:`~cai.client.event.Event`
            object should be returned.
    """
    if cmd in HANDLERS:
        logger.warning(
            f"You are overwriting an existing handler for command {cmd}!"
        )
    HANDLERS[cmd] = packet_handler


__all__ = [
    "get_client",
    "close",
    "close_all",
    "login",
    "submit_captcha",
    "submit_slider_ticket",
    "request_sms",
    "submit_sms",
    "register_packet_handler",
]
