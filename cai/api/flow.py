"""Application Flow APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import TYPE_CHECKING, Callable, Awaitable

from cai.log import logger
from cai.client import HANDLERS, Event, Client, Command, IncomingPacket

from .base import BaseAPI

if TYPE_CHECKING:
    from .client import Client as Client_T


class Events(BaseAPI):
    def add_event_listener(
        self, listener: Callable[["Client_T", Event], Awaitable[None]]
    ):
        """Add event listener.

        Args:
            listener (Callable[[Client, Event], Awaitable[None]]): Event listener.
        """
        self.client.add_event_listener(lambda _, e: listener(self, e))  # type: ignore

    def register_packet_handler(
        self,
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
