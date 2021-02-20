from typing import Dict, Optional

from cai.client import Client

_clients: Dict[int, Client] = {}


def _get_client(uin: Optional[int] = None) -> Client:
    if not _clients:
        raise RuntimeError(f"No client available!")
    elif len(_clients) == 1 and not uin:
        return list(_clients.values())[0]
    else:
        if not uin:
            raise RuntimeError(
                f"Multiple clients found! Specify uin to choose."
            )
        if uin not in _clients:
            raise RuntimeError(f"Client {uin} not exists!")
        return _clients[uin]


async def login(uin: int, password_md5: bytes):
    if uin in _clients:
        client = _clients[uin]
    client = Client(uin, password_md5)
    if client.connected:
        raise RuntimeError(f"Client {uin} already connected!")
    await client.connect()
    try:
        await client.login()
    except Exception:
        await client.disconnect()
        raise
    _clients[uin] = client


__all__ = ["login"]
