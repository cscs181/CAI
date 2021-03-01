from typing import Dict, Optional

from cai.client import Client
from cai.exceptions import ApiException, ClientNotAvailable

_clients: Dict[int, Client] = {}


def _get_client(uin: Optional[int] = None) -> Client:
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
        raise ClientNotAvailable(f"No client available!")
    elif len(_clients) == 1 and not uin:
        return list(_clients.values())[0]
    else:
        if not uin:
            raise ClientNotAvailable(
                f"Multiple clients found! Specify uin to choose."
            )
        if uin not in _clients:
            raise ClientNotAvailable(f"Client {uin} not exists!")
        return _clients[uin]


async def close(uin: Optional[int] = None) -> None:
    """Close an existing client.

    Args:
        uin (Optional[int], optional): Account of the client want to close. Defaults to None.
    """
    client = _get_client(uin)
    await client.close()


async def login(uin: int, password_md5: bytes) -> Client:
    """Create a new client (or use an existing one) and login.

    This function wraps the login method of the client.

    Args:
        uin (int): QQ account number.
        password_md5 (bytes): md5 bytes of the password.

    Raises:
        RuntimeError: Client already exists and is running.
        LoginSliderException: Need slider ticket.
        LoginCaptchaException: Need captcha image.
    """
    if uin in _clients:
        client = _clients[uin]
        if client.connected:
            raise RuntimeError(f"Client {uin} already connected!")
        client._password_md5 = password_md5
    client = Client(uin, password_md5)
    _clients[uin] = client
    await client.connect()
    try:
        await client.login()
    except ApiException:
        raise
    except Exception:
        await client.close()
        raise
    return client


async def submit_captcha(
    captcha: str, captcha_sign: bytes, uin: Optional[int] = None
) -> bool:
    client = _get_client(uin)
    try:
        await client.submit_captcha(captcha, captcha_sign)
    except ApiException:
        raise
    except Exception:
        await client.close()
        raise
    return True


async def submit_slider_ticket(ticket: str, uin: Optional[int] = None) -> bool:
    client = _get_client(uin)
    try:
        await client.submit_slider_ticket(ticket)
    except ApiException:
        raise
    except Exception:
        await client.close()
        raise
    return True


__all__ = [
    "_get_client", "close", "login", "submit_captcha", "submit_slider_ticket"
]
