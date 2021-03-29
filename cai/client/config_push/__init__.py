"""ConfigPushSvc Related SDK.

This module is used to build and handle config push service related packet.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""

from typing import TYPE_CHECKING

from jce import types

from cai.log import logger
from .jce import PushResp, FileServerPushList
from cai.utils.jce import RequestPacketVersion3
from cai.client.packet import UniPacket, IncomingPacket
from .event import (
    ConfigPushEvent, _ConfigPushEventBase, SsoServerPushEvent,
    FileServerPushEvent, LogActionPushEvent
)

if TYPE_CHECKING:
    from cai.client import Client


def encode_config_push_response(
    uin: int, seq: int, session_id: bytes, d2key: bytes, type: int,
    jcebuf: bytes, large_seq: int
):
    """Build config push response packet.

    command name: `ConfigPushSvc.PushResp`

    Note:
        Source: com.tencent.mobileqq.msf.core.a.c.b

    Args:
        uin (int): User QQ number.
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        d2key (bytes): Siginfo d2 key.
        type (int): ConfigPushSvc request type.
        jcebuf (bytes): ConfigPushSvc request jcebuf.
        large_seq (int): ConfigPushSvc request large_seq.
    """
    COMMAND_NAME = "ConfigPushSvc.PushResp"

    resp = PushResp(
        type=type, jcebuf=jcebuf if type == 3 else None, large_seq=large_seq
    )
    payload = PushResp.to_bytes(0, resp)
    resp_packet = RequestPacketVersion3(
        servant_name="QQService.ConfigPushSvc.MainServant",
        func_name="PushResp",
        data=types.MAP({types.STRING("PushResp"): types.BYTES(payload)})
    ).encode()
    packet = UniPacket.build(
        uin, seq, COMMAND_NAME, session_id, 1, resp_packet, d2key
    )
    return packet


# ConfigPushSvc.PushReq
async def handle_config_push_request(
    client: "Client", packet: IncomingPacket
) -> ConfigPushEvent:
    event = ConfigPushEvent.decode_push_req(
        packet.uin, packet.seq, packet.ret_code, packet.command_name,
        packet.data
    )
    if isinstance(event, SsoServerPushEvent):
        logger.debug(f"ConfigPush: Got new server addresses.")
    elif isinstance(event, FileServerPushEvent):
        client._file_storage_info = event.list

    if isinstance(event, _ConfigPushEventBase):
        seq = client.next_seq()
        resp_packet = encode_config_push_response(
            client.uin, seq, client._session_id, client._siginfo.d2key,
            event.type, event.jcebuf, event.large_seq
        )
        client.send(seq, "ConfigPushSvc.PushResp", resp_packet)

    return event


__all__ = [
    "decode_push_req", "FileServerPushList", "ConfigPushEvent",
    "SsoServerPushEvent", "FileServerPushEvent", "LogActionPushEvent"
]
