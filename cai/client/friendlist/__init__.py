"""Friend List Related SDK.

This module is used to build and handle friend list related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
from typing import Optional, TYPE_CHECKING

from jce import types

from cai.utils.binary import Packet
from cai.pb.im.oidb.cmd0xd50 import ReqBody
from cai.utils.jce import RequestPacketVersion3
from cai.client.packet import UniPacket, IncomingPacket
from .jce import (
    FriendListReq,
    TroopListReqV2Simplify,
    TroopMemberListReq,
)
from .event import (
    FriendListEvent,
    FriendListSuccess,
    FriendListFail,
    TroopListEvent,
    TroopListSuccess,
    TroopListFail,
    TroopMemberListEvent,
    TroopMemberListSuccess,
    TroopMemberListFail,
)


if TYPE_CHECKING:
    from cai.client import Client


def encode_get_friend_list(
    seq: int,
    session_id: bytes,
    uin: int,
    d2key: bytes,
    friend_index: int = 0,
    friend_count: int = 0,
    group_index: int = 0,
    group_count: int = 0,
) -> Packet:
    """Build get friend list packet.

    Called in ``com.tencent.mobileqq.service.friendlist.FriendListService.k``.

    command name: ``friendlist.GetFriendListReq``

    Note:
        Source: com.tencent.mobileqq.service.friendlist.FriendListService.m

    Args:
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        uin (int): User QQ number.
        d2key (bytes): Siginfo d2 key.
        friend_index (int): Start index of friend list.
        friend_count (int): Number of friends to list.
        group_index (int): Start index of group list.
        group_count (int): Number of groups to list.

    Returns:
        Packet: GetFriendListReq packet.
    """
    COMMAND_NAME = "friendlist.GetFriendListReq"

    req = FriendListReq(
        request_type=3,
        if_reflush=friend_index <= 0,
        uin=uin,
        start_index=friend_index,
        friend_count=friend_count,
        group_id=bytes(1),
        if_get_group_info=group_count > 0,
        group_start_index=group_index,
        group_count=group_count,
        if_get_msf_group=False,
        if_show_term_type=True,
        version=31,
        d50_req=ReqBody(
            appid=1002,
            req_music_switch=1,
            req_mutualmark_alienation=1,
            req_ksing_switch=1,
            req_mutualmark_lbsshare=1,
            req_aio_quick_app=1,
        ).SerializeToString(),
        sns_type_list=[13580, 13581, 13582],
    )
    payload = FriendListReq.to_bytes(0, req)
    req_packet = RequestPacketVersion3(
        servant_name="mqq.IMService.FriendListServiceServantObj",
        func_name="GetFriendListReq",
        data=types.MAP({types.STRING("FL"): types.BYTES(payload)}),
    ).encode()
    packet = UniPacket.build(
        uin, seq, COMMAND_NAME, session_id, 1, req_packet, d2key
    )
    return packet


async def handle_friend_list(
    client: "Client", packet: IncomingPacket
) -> "FriendListEvent":
    return FriendListEvent.decode_response(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
    )


def encode_get_troop_list(
    seq: int,
    session_id: bytes,
    uin: int,
    d2key: bytes,
    cookies: Optional[bytes] = None,
) -> Packet:
    """Build get troop list v2 simplified packet.

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
        Packet: GetTroopListReqV2 simplified packet.
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


def encode_get_troop_member_list(
    seq: int,
    session_id: bytes,
    uin: int,
    d2key: bytes,
    group_uin: int,
    group_code: int,
    next_uin: int = 0,
) -> Packet:
    """Build get troop member list packet.

    Called in ``com.tencent.mobileqq.troop.handler.TroopMemberInfoHandler.a``.

    command name: ``friendlist.GetTroopMemberListReq``

    Note:
        Source: com.tencent.mobileqq.service.troop.TroopSender.c

    Args:
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        uin (int): User QQ number.
        d2key (bytes): Siginfo d2 key.
        group_uin (int): Group uin number.
        group_code (int): Group code number.
        next_uin (int, optional): Next uin number. Defaults to 0.

    Returns:
        Packet: getTroopMemberList simplified packet.
    """
    COMMAND_NAME = "friendlist.GetTroopMemberListReq"

    req = TroopMemberListReq(
        uin=uin,
        group_code=group_code,
        next_uin=next_uin,
        group_uin=group_uin,
        version=3,
    )
    payload = TroopMemberListReq.to_bytes(0, req)
    req_packet = RequestPacketVersion3(
        servant_name="mqq.IMService.FriendListServiceServantObj",
        func_name="GetTroopMemberListReq",
        data=types.MAP({types.STRING("GTML"): types.BYTES(payload)}),
    ).encode()
    packet = UniPacket.build(
        uin, seq, COMMAND_NAME, session_id, 1, req_packet, d2key
    )
    return packet


async def handle_troop_member_list(
    client: "Client", packet: IncomingPacket
) -> TroopMemberListEvent:
    return TroopMemberListEvent.decode_response(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
    )


__all__ = [
    "encode_get_friend_list",
    "handle_friend_list",
    "encode_get_troop_list",
    "handle_troop_list",
    "encode_get_troop_member_list",
    "handle_troop_member_list",
    "FriendListEvent",
    "FriendListSuccess",
    "FriendListFail",
    "TroopListEvent",
    "TroopListSuccess",
    "TroopListFail",
    "TroopMemberListEvent",
    "TroopMemberListSuccess",
    "TroopMemberListFail",
]
