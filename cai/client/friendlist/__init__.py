"""Friend List Related SDK.

This module is used to build and handle friend list related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
from typing import Optional, TYPE_CHECKING

from jce import types

from .event import (
    TroopListEvent,
    TroopListSuccess,
    TroopListFail,
)
from cai.utils.binary import Packet
from cai.utils.jce import RequestPacketVersion3
from .jce import StTroopNum, TroopListReqV2Simplify
from cai.client.packet import UniPacket, IncomingPacket


if TYPE_CHECKING:
    from cai.client import Client


def encode_get_troop_list(
    seq: int,
    session_id: bytes,
    uin: int,
    d2key: bytes,
    cookies: Optional[bytes] = None,
) -> Packet:
    """Build get troop list v2 packet.

    Called in ``com.tencent.mobileqq.troop.handler.TroopListHandler.a``.

    command name: ``friendlist.GetTroopListReqV2``

    Note:
        Source: com.tencent.mobileqq.service.troop.TroopSender.b

    Args:
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        uin (int): User QQ number.
        d2key (bytes): Siginfo d2 key.
        cookies (Optional[bytes], optional): Cookie vector. Defaults to None.

    Returns:
        Packet: Register packet.
    """
    COMMAND_NAME = "friendlist.GetTroopListReqV2"

    req = TroopListReqV2Simplify(
        uin=uin,
        get_msf_msg_flag=False,
        cookies=cookies,
        group_flag_ext=bytes([1]),
        version=9,
        version_num=1,
        get_long_group_name=True,
    )
    payload = TroopListReqV2Simplify.to_bytes(0, req)
    req_packet = RequestPacketVersion3(
        servant_name="mqq.IMService.FriendListServiceServantObj",
        func_name="GetTroopListReqV2Simplify",
        data=types.MAP(
            {types.STRING("GetTroopListReqV2Simplify"): types.BYTES(payload)}
        ),
    ).encode()
    packet = UniPacket.build(
        uin, seq, COMMAND_NAME, session_id, 1, req_packet, d2key
    )
    return packet


async def handle_troop_list(
    client: "Client", packet: IncomingPacket
) -> TroopListEvent:
    return TroopListEvent.decode_response(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
    )


__all__ = [
    "encode_get_troop_list",
    "handle_troop_list",
    "TroopListEvent",
    "TroopListSuccess",
    "TroopListFail",
    "StTroopNum",
]
