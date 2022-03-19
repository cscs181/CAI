"""Client Base Command.

This module is used to build command from packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
from typing import TYPE_CHECKING
from dataclasses import dataclass

from .packet import IncomingPacket

if TYPE_CHECKING:
    from .client import Client


@dataclass
class Command:
    uin: int
    seq: int
    ret_code: int
    command_name: str


@dataclass
class UnhandledCommand(Command):
    data: bytes


async def _packet_to_command(
    client: "Client", packet: IncomingPacket, _device
) -> UnhandledCommand:
    return UnhandledCommand(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
    )
