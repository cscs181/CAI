"""Heartbeat Related SDK.

This module is used to build and handle heartbeat related packet.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""

from typing import TYPE_CHECKING
from dataclasses import dataclass

from cai.client.event import Event
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol
from cai.client.packet import CSsoBodyPacket, CSsoDataPacket, IncomingPacket

if TYPE_CHECKING:
    from cai.client import Client

DEVICE = get_device()
APK_INFO = get_protocol()


def encode_heartbeat(seq: int, session_id: bytes, ksid: bytes, uin: int):
    """Build heartbeat alive packet.

    Called in `com.tencent.mobileqq.msf.core.C26002ac.A`.

    command name: `Heartbeat.Alive`

    Note:
        Source: oicq.wlogin_sdk.request.n

    Args:
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.

    Returns:
        Packet: Login packet.
    """
    COMMAND_NAME = "Heartbeat.Alive"

    SUB_APP_ID = APK_INFO.sub_app_id

    sso_packet = CSsoBodyPacket.build(
        seq, SUB_APP_ID, COMMAND_NAME, DEVICE.imei, session_id, ksid, bytes()
    )
    packet = CSsoDataPacket.build(uin, 0, sso_packet, key=None)
    return packet


@dataclass
class Heartbeat(Event):
    pass


async def decode_heartbeat(
    client: "Client", packet: IncomingPacket
) -> Heartbeat:
    return Heartbeat(
        packet.uin, packet.seq, packet.ret_code, packet.command_name
    )


__all__ = ["encode_heartbeat", "decode_heartbeat", "Heartbeat"]
