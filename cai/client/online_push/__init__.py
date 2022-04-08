"""OnlinePush Related SDK.

This module is used to build and handle online push related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
from typing import TYPE_CHECKING, List, Tuple, Optional, Sequence

from jce import JceStruct, JceDecoder, types

from cai.log import logger
from cai.client import events
from cai.utils.binary import Packet
from cai.client.message_service import MESSAGE_DECODERS
from cai.client.packet import UniPacket, IncomingPacket
from cai.utils.jce import RequestPacket, RequestPacketVersion3
from cai.pb.im.oidb.cmd0x857.troop_tips import TemplParam, NotifyMsgBody
from cai.pb.im.op.online_push_pb2 import DelMsgCookies

from .jce import DelMsgInfo, DeviceInfo, SvcRespPushMsg, SvcReqPushMsg
from .command import PushMsg, PushMsgError, PushMsgCommand

if TYPE_CHECKING:
    from cai.client import Client


# OnlinePush.RespPush
def encode_push_response(
    seq: int,
    session_id: bytes,
    uin: int,
    d2key: bytes,
    svrip: int,
    delete_messages: List[DelMsgInfo] = [],
    push_token: Optional[bytes] = None,
    service_type: int = 0,
    device_info: Optional[DeviceInfo] = None,
    req_id: int = 0
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
        req_id=req_id,
        servant_name="OnlinePush",
        func_name="SvcRespPushMsg",
        data=types.MAP({types.STRING("resp"): types.BYTES(payload)}),
    ).encode()
    packet = UniPacket.build(
        uin, seq, COMMAND_NAME, session_id, 1, req_packet, d2key
    )
    return packet


async def handle_c2c_sync(
    client: "Client", packet: IncomingPacket
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
) -> PushMsgCommand:
    """Handle Push Message Command.

    Note:
        Source: troop 1001, c2c 1001, discussion 1001

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
                    push.push.svrip,
                    push_token=push.push.push_token or None,
                    service_type=1,
                    device_info=DeviceInfo(
                        net_type=1,
                        dev_type=client.device.model,
                        os_ver=client.device.version.release,
                        vendor_name=client.device.vendor_name,
                        vendor_os_name=client.device.vendor_os_name,
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
            res["sender"] = int(p.value)
        elif p.name == "uin_str2":
            res["target"] = int(p.value)
        elif p.name == "suffix_str":
            res["suffix"] = p.value
        elif p.name == "action_str":
            res["action"] = p.value
    return res


repeat_ev = set()

# OnlinePush.ReqPush
async def handle_req_push(
    client: "Client", packet: IncomingPacket
) -> PushMsgCommand:
    req_pkg = RequestPacket.decode(packet.data)

    # sbtx
    if req_pkg.req_id in repeat_ev:
        repeat_ev.remove(req_pkg.req_id)
        return PushMsgCommand(packet.uin, packet.seq, packet.ret_code, packet.command_name)
    else:
        repeat_ev.add(req_pkg.req_id)

    body = SvcReqPushMsg.decode(
        JceDecoder.decode_single(req_pkg.buffer)[1]["req"]["OnlinePushPack.SvcReqPushMsg"]  # type: ignore
    ).body

    _uin, stime, push_type, content = (
        body.uin,
        body.msg_time,
        body.msg_info[0].msg_type,
        body.msg_info[0].msg,
    )

    if push_type == 732:  # group
        gid = int.from_bytes(content[0:4], "big")
        stype = content[4]
        if stype in (0x14, 0x11):
            notify = NotifyMsgBody.FromString(content[7:])
            if stype == 0x14:  # nudge
                client.dispatch_event(
                    events.NudgeEvent(
                        **_parse_poke(notify.general_gray_tip.templ_param),
                        group=gid,
                    )
                )
            elif stype == 0x11:  # recall
                msg = notify.recall.recalled_msg_list[0]
                client.dispatch_event(
                    events.MemberRecallMessageEvent(
                        gid,
                        notify.recall.uin,
                        notify.recall.op_type,
                        msg.author_uin,
                        msg.msg_random,
                        msg.seq,
                        msg.time,
                    )
                )
        elif stype == 0x0C:  # mute event
            operator = int.from_bytes(content[6:10], "big", signed=False)
            target = int.from_bytes(content[16:20], "big", signed=False)
            duration = int.from_bytes(content[20:24], "big", signed=False)
            if duration > 0:  # muted
                client.dispatch_event(
                    events.MemberMutedEvent(gid, operator, target, duration)
                )
            else:
                client.dispatch_event(
                    events.MemberUnMutedEvent(gid, operator, target)
                )
    elif push_type == 528:
        pass
        # TODO: parse friend event

    seq = client.next_seq()
    pkg = encode_push_response(
        seq,
        client._session_id,
        _uin,
        client._siginfo.d2key,
        body.svrip,
        [
            DelMsgInfo(
                from_uin=info.from_uin,
                msg_seq=info.msg_seq,
                msg_time=info.msg_time,
                msg_cookies=DelMsgCookies(
                    msg_type=info.msg_type,
                    msg_uid=info.msg_uid,
                    type=3,
                    xid=50015
                ).SerializeToString()
            ) for info in body.msg_info
        ],
        req_id=req_pkg.req_id
    )

    # FIXME: useless
    await client.send(seq, "OnlinePush.RespPush", pkg)

    return PushMsgCommand(
        packet.uin, packet.seq, packet.ret_code, packet.command_name
    )


__all__ = [
    "handle_c2c_sync",
    "handle_push_msg",
    "PushMsgCommand",
    "PushMsg",
    "PushMsgError",
]
