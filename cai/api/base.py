from typing import Callable

from cai.client.client import Client as client_t
from cai.exceptions import LoginException


class BaseAPI:
    client: client_t

    async def _executor(self, func_name: str, *args, **kwargs):
        if not hasattr(self.client, func_name):
            raise AttributeError(f"client has no attribute '{func_name}'")
        try:
            await getattr(self.client, func_name)(*args, **kwargs)
        except LoginException:
            raise
        except Exception:
            await self.client.close()
            raise
