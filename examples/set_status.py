"""Example Code for Set Client Status.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import os
import signal
import asyncio
from hashlib import md5

import cai
from cai.client import OnlineStatus


async def run():
    try:
        account = os.getenv("ACCOUNT", "")
        password = os.getenv("PASSWORD")
        account = int(account)
        assert password
    except Exception:
        print(
            f"Error: account '{account}', password '{password}'"  # type: ignore
        )
        return

    client = await cai.login(account, md5(password.encode()).digest())

    await asyncio.sleep(10)
    await cai.set_status(OnlineStatus.Qme)
    print("Current client status: ", client.status)


if __name__ == "__main__":
    close = asyncio.Event()

    async def wait_cleanup():
        await close.wait()
        await cai.close_all()

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, close.set)
    loop.add_signal_handler(signal.SIGTERM, close.set)
    loop.create_task(run())
    loop.run_until_complete(wait_cleanup())
