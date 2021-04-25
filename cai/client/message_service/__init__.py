"""MessageSvc Related SDK.

This module is used to build and handle message service related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import TYPE_CHECKING

from cai.utils.binary import Packet
from cai.client.packet import IncomingPacket

if TYPE_CHECKING:
    from cai.client import Client


# TODO
async def encode_get_message() -> Packet:
    ...


# TODO
async def handle_push_notify(client: "Client", packet: IncomingPacket):
    ...
