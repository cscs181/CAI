"""Client Base Events.

This module is used to build event from packet.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
from dataclasses import dataclass

from .packet import IncomingPacket


@dataclass
class Event:
    uin: int
    seq: int
    ret_code: int
    command_name: str


@dataclass
class UnhandledEvent(Event):
    data: bytes


def _packet_to_event(packet: IncomingPacket) -> UnhandledEvent:
    return UnhandledEvent(
        packet.uin, packet.seq, packet.ret_code, packet.command_name,
        packet.data
    )
