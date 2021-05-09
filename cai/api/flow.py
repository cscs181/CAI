"""Application Flow APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional, Callable, Awaitable

from cai.log import logger
from .client import get_client
from cai.client import (
    Client,
    HANDLERS,
    Event,
    Command,
    IncomingPacket,
)


def add_event_listener(
    listener: Callable[[Client, Event], Awaitable[None]],
    uin: Optional[int] = None,
):
    """Add event listener.

    If uin is ``None``, listener will receive events from all clients.

    Args:
        listener (Callable[[Client, Event], Awaitable[None]]): Event listener.
        uin (Optional[int], optional): Account of the client want to listen.
            Defaults to None.
    """
    if uin:
        client = get_client(uin)
        client.add_event_listener(listener)
    else:
        Client.LISTENERS.add(listener)


def register_packet_handler(
    cmd: str,
    packet_handler: Callable[[Client, IncomingPacket], Awaitable[Command]],
) -> None:
    """Register custom packet handler.

    Note:
        This function is a low-level api to mock default behavior.
        Be aware of what you are doing!

    Args:
        cmd (str): Command name of the packet.
        packet_handler (Callable[[Client, IncomingPacket], Awaitable[Command]]):
            Asynchronous packet handler. A :obj:`~cai.client.command.Command`
            object should be returned.
    """
    if cmd in HANDLERS:
        logger.warning(
            f"You are overwriting an existing handler for command {cmd}!"
        )
    HANDLERS[cmd] = packet_handler
