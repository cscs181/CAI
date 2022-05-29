from cai.client.client import Client as client_t


class BaseAPI:
    client: client_t

    async def _executor(
        self, func_name: str, *args, uncaught_error=False, **kwargs
    ):
        if not hasattr(self.client, func_name):
            raise AttributeError(f"client has no attribute '{func_name}'")
        try:
            return await getattr(self.client, func_name)(*args, **kwargs)
        except Exception:
            if uncaught_error:
                await self.client.close()
            raise
