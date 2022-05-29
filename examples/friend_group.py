"""Example Code for Friend/Group.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import os
import signal
import asyncio
from hashlib import md5

from cai.api.client import Client


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

    client = Client()
    client = await cai.login(account, md5(password.encode()).digest())

    # friend
    friend_list = await cai.get_friend_list()
    friend_group_list = await cai.get_friend_group_list()
    print("========== friends ==========", *friend_list, sep="\n")
    print("========== friend groups ==========", *friend_group_list, sep="\n")
    example_friend = friend_list[0]
    # friend = await cai.get_friend(friend_uin)
    print("========== example friend ==========")
    print("uin: ", example_friend.uin)
    print("nick: ", example_friend.nick)
    print("remark: ", example_friend.remark)
    print("group: ", await example_friend.get_group())

    group_list = await cai.get_group_list()
    print("\n========== group list ==========", *group_list, sep="\n")
    example_group = group_list[0]
    # group = await cai.get_group(group_id)
    print("========== example group ==========")
    print("group id: ", example_group.group_id)
    print("group name: ", example_group.group_name)
    print("group owner: ", example_group.group_owner_uin)
    example_group_member_list = await example_group.get_members()
    print(
        "========== example group members ==========",
        *example_group_member_list,
        sep="\n",
    )


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
