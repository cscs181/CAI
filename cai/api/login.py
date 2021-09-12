"""Application Login APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional

from cai.client import Client
from cai.exceptions import LoginException

from . import _clients
from .client import get_client


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
