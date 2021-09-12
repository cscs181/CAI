"""Example Code for Message.

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
from cai.client import Event, Client, GroupMessage, PrivateMessage


async def run():
    account = os.getenv("ACCOUNT", "")
    password = os.getenv("PASSWORD")
    try:
        account = int(account)
        assert password
    except Exception:
        print(
            f"Error: account '{account}', password '{password}'"  # type: ignore
        )
        return

    client = await cai.login(account, md5(password.encode()).digest())

    cai.add_event_listener(listen_message)
    # cai.add_event_listener(listen_message, uin=account)
    # client.add_event_listener(listen_message)


async def listen_message(client: Client, event: Event):
    if isinstance(event, PrivateMessage):
        print("Private Message received from", event.from_uin)
        print("Private Message elements:", event.message)
    elif isinstance(event, GroupMessage):
        print(
            f"Group Message received from {event.group_name}({event.group_id})"
        )
        print("Group Message elements:", event.message)


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
