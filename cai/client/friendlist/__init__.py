"""Friend List Related SDK.

This module is used to build and handle friend list related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
from typing import TYPE_CHECKING

from cai.client.event import Event
from cai.utils.binary import Packet
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol
from cai.utils.jce import RequestPacketVersion3
from cai.client.packet import UniPacket, IncomingPacket

if TYPE_CHECKING:
    from cai.client import Client


def encode_get_troop_list() -> Packet:
    ...


def handle_troop_list(client: "Client", packet: IncomingPacket):
    ...


__all__ = ["encode_get_troop_list", "handle_troop_list"]
