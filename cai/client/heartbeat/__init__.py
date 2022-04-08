"""Heartbeat Related SDK.

This module is used to build and handle heartbeat related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import TYPE_CHECKING
from dataclasses import dataclass

from cai.utils.binary import Packet
from cai.client.command import Command
from cai.client.packet import CSsoBodyPacket, CSsoDataPacket, IncomingPacket

if TYPE_CHECKING:
    from cai.client import Client


def encode_heartbeat(
    seq: int,
    session_id: bytes,
    imei: str,
    ksid: bytes,
    uin: int,
    sub_app_id: int,
) -> Packet:
    """Build heartbeat alive packet.

    Called in `com.tencent.mobileqq.msf.core.C26002ac.A`.

    command name: `Heartbeat.Alive`

    Note:
        Source: oicq.wlogin_sdk.request.n

    Args:
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        imei (str): Device imei.
        uin (int): User QQ number.
        sub_app_id (int): apkinfo

    Returns:
        Packet: Login packet.
    """
    COMMAND_NAME = "Heartbeat.Alive"

    SUB_APP_ID = sub_app_id

    sso_packet = CSsoBodyPacket.build(
        seq, SUB_APP_ID, COMMAND_NAME, imei, session_id, ksid, bytes()
    )
    packet = CSsoDataPacket.build(uin, 0, sso_packet, key=None)
    return packet


@dataclass
class Heartbeat(Command):
    pass


async def handle_heartbeat(
    client: "Client", packet: IncomingPacket
) -> Heartbeat:
    return Heartbeat(
        packet.uin, packet.seq, packet.ret_code, packet.command_name
    )


__all__ = ["encode_heartbeat", "handle_heartbeat", "Heartbeat"]
