"""OnlinePush Related SDK.

This module is used to build and handle online push related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import struct
import tkinter
from typing import TYPE_CHECKING, List, Tuple, Optional, Sequence

from jce import types, JceDecoder

from cai.log import logger
from cai.utils.binary import Packet
from cai.utils.jce import RequestPacketVersion3, RequestPacket
from cai.client.message_service import MESSAGE_DECODERS
from cai.client.packet import UniPacket, IncomingPacket
from cai.settings.device import DeviceInfo as _DeviceInfo_t
from cai.pb.im.oidb.group0x857.group0x857_pb2 import NotifyMsgBody, TemplParam

from .. import events
from ...settings.protocol import ApkInfo
from .jce import DelMsgInfo, DeviceInfo, SvcRespPushMsg
from .command import PushMsg, PushMsgError, PushMsgCommand

if TYPE_CHECKING:
    from cai.client import Client


def encode_push_response(
    seq: int,
    session_id: bytes,
    uin: int,
    d2key: bytes,
    resp_uin: int,  # warn: unused var
    svrip: int,
    delete_messages: List[DelMsgInfo] = [],
    push_token: Optional[bytes] = None,
    service_type: int = 0,
    device_info: Optional[DeviceInfo] = None,
) -> Packet:
    """Build online push response packet.

    Called in ``com.tencent.mobileqq.app.BaseMessageHandler.a``.

    command name: ``OnlinePush.RespPush``

    Note:
        Source: com.tencent.mobileqq.service.message.MessageFactorySender.b

    Args:
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        uin (int): User QQ number.
        d2key (bytes): Siginfo d2 key.
        resp_uin (int): Push response uin.
        svrip (int): Svrip from push packet.
        delete_messages (List[DelMsgInfo]): List of delete messages.
        push_token (Optional[bytes]): Push token from push packet.
        service_type (int): Service type.
        device_info (Optional[DeviceInfo]): Device info.

    Returns:
        Packet: PbDeleteMsg packet.
    """
    COMMAND_NAME = "OnlinePush.RespPush"

    resp = SvcRespPushMsg(
        uin=uin,
        del_infos=delete_messages,
        svrip=svrip,
        push_token=push_token,
        service_type=service_type,
        device_info=device_info,
    )
    payload = SvcRespPushMsg.to_bytes(0, resp)
    req_packet = RequestPacketVersion3(
        servant_name="OnlinePush",
        func_name="SvcRespPushMsg",
        data=types.MAP({types.STRING("resp"): types.BYTES(payload)}),
    ).encode()
    packet = UniPacket.build(
        uin, seq, COMMAND_NAME, session_id, 1, req_packet, d2key
    )
    return packet


async def handle_c2c_sync(
    client: "Client", packet: IncomingPacket, _device
) -> PushMsgCommand:
    """Handle C2C Message Sync.

    Note:
        Source: c2c 2003

        com.tencent.imcore.message.C2CMessageProcessor.b (handleMsgPush_PB_SlaveMaster)

        com.tencent.mobileqq.app.MessageHandler.b
    """
    push = PushMsgCommand.decode_response(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
    )
    if isinstance(push, PushMsg) and push.push.HasField("msg"):
        # c2c 2003
        message = push.push.msg
        msg_type = message.head.type

        resp_packet = encode_push_response(
            push.seq,
            client._session_id,
            client.uin,
            client._siginfo.d2key,
            message.head.from_uin,
            push.push.svrip,
            push_token=push.push.push_token or None,
        )
        await client.send(push.seq, "OnlinePush.RespPush", resp_packet)

        Decoder = MESSAGE_DECODERS.get(msg_type, None)
        if not Decoder:
            logger.debug(
                f"{push.command_name}: "
                f"Received unknown message type {msg_type}."
            )
            return push
        decoded_message = Decoder(message)
        if decoded_message:
            client.dispatch_event(decoded_message)

    return push


async def handle_push_msg(
    client: "Client",
    packet: IncomingPacket,
    device: Tuple[_DeviceInfo_t, ApkInfo],
) -> PushMsgCommand:
    """Handle Push Message Command.

    Note:
        Source: troop 1001, c2c 1001, discussion 1001

        com.tencent.mobileqq.app.MessageHandler.b
    """
    device = device[0]

    push = PushMsgCommand.decode_response(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
    )
    if isinstance(push, PushMsg) and push.push.HasField("msg"):
        message = push.push.msg
        msg_type = message.head.type

        if msg_type == 43 or msg_type == 82:
            # troop 1001
            # ping
            if push.push.ping_flag == 1:
                resp_packet = encode_push_response(
                    push.seq,
                    client._session_id,
                    client.uin,
                    client._siginfo.d2key,
                    client.uin,
                    push.push.svrip,
                    push_token=push.push.push_token or None,
                    service_type=1,
                    device_info=DeviceInfo(
                        net_type=1,
                        dev_type=device.model,
                        os_ver=device.version.release,
                        vendor_name=device.vendor_name,
                        vendor_os_name=device.vendor_os_name,
                    ),
                )
                await client.send(push.seq, "OnlinePush.RespPush", resp_packet)
        elif msg_type == 141:
            # c2c 1001
            delete_info = DelMsgInfo(
                from_uin=message.head.from_uin,
                msg_seq=message.head.seq,
                msg_time=message.head.time,
            )
            resp_packet = encode_push_response(
                push.seq,
                client._session_id,
                client.uin,
                client._siginfo.d2key,
                message.head.from_uin,
                push.push.svrip,
                [delete_info],
                push_token=push.push.push_token or None,
            )
            await client.send(push.seq, "OnlinePush.RespPush", resp_packet)
        elif msg_type != 42:
            # discussion 1001
            pass

        Decoder = MESSAGE_DECODERS.get(msg_type, None)
        if not Decoder:
            logger.debug(
                f"{push.command_name}: "
                f"Received unknown message type {msg_type}."
            )
            return push
        decoded_message = Decoder(message)
        if decoded_message:
            client.dispatch_event(decoded_message)

    return push


def _parse_poke(params: Sequence[TemplParam]) -> dict:
    res = {"target": None, "sender": None, "action": None, "suffix": None}
    for p in params:
        if p.name == "uin_str1":
            res["sender"] = p.value
        elif p.name == "uin_str2":
            res["target"] = p.value
        elif p.name == "suffix_str":
            res["suffix"] = p.value
        elif p.name == "action_str":
            res["action"] = p.value
    return res



# OnlinePush.ReqPush
async def handle_req_push(
    client: "Client",
    packet: IncomingPacket,
    device: Tuple[_DeviceInfo_t, ApkInfo],
) -> PushMsgCommand:
    data = JceDecoder.decode_single(  # type: ignore
        RequestPacket.decode(packet.data).buffer
    )[1]["req"]["OnlinePushPack.SvcReqPushMsg"]
    body = JceDecoder.decode_bytes(data)[0]
    _, stime, content = body[0], body[1], body[2][0][6]
    # TODO: Send OnlinePush.RespPush
    if body[2][0][2] == 732:  # group
        gid = int.from_bytes(content[0:4], "big")
        dtype = content[4]
        if dtype in (0x14, 0x11):
            notify = NotifyMsgBody.FromString(content[7:])
            if dtype == 0x14:  # nudge
                client.dispatch_event(events.NudgeEvent(
                    **_parse_poke(notify.optGeneralGrayTip.msgTemplParam),
                    group=gid
                ))
            elif dtype == 0x11:  # recall
                msg = notify.optMsgRecall.recalledMsgList[0]
                client.dispatch_event(events.MemberRecallMessageEvent(
                    gid,
                    notify.optMsgRecall.uin,
                    notify.optMsgRecall.opType,
                    msg.authorUin,
                    msg.msgRandom,
                    msg.seq,
                    msg.time
                ))
        elif dtype == 0x0c:  # mute event
            operator = int.from_bytes(content[6:10], "big", signed=False)
            target = int.from_bytes(content[16:20], "big", signed=False)
            duration = int.from_bytes(content[20:24], "big", signed=False)
            if duration > 0:  # muted
                client.dispatch_event(events.MemberMutedEvent(
                    gid,
                    operator,
                    target,
                    duration
                ))
            else:
                client.dispatch_event(events.MemberUnMutedEvent(
                    gid,
                    operator,
                    target
                ))
    # TODO: parse friend event
    return PushMsgCommand(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name
    )


__all__ = [
    "handle_c2c_sync",
    "handle_push_msg",
    "PushMsgCommand",
    "PushMsg",
    "PushMsgError",
]
