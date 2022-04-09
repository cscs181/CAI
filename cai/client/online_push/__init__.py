"""OnlinePush Related SDK.

This module is used to build and handle online push related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
from typing import TYPE_CHECKING, List, Optional, Sequence

from jce import types

from cai.log import logger
from cai.client import events
from cai.utils.binary import Packet
from cai.utils.jce import RequestPacketVersion3
from cai.client.message_service import MESSAGE_DECODERS
from cai.client.packet import UniPacket, IncomingPacket
from cai.pb.im.oidb.cmd0x857.troop_tips import TemplParam, NotifyMsgBody

from .jce import DelMsgInfo, DeviceInfo, SvcRespPushMsg
from .command import (
    PushMsg,
    SvcReqPush,
    PushMsgError,
    PushMsgCommand,
    SvcReqPushCommand,
)

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
    req_id: int = 0,
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


def _parse_poke(params: Sequence[TemplParam], default: int) -> dict:
    res = {"target": None, "sender": None, "action": None, "suffix": None}
    for p in params:
        name, value = p.name.decode(), p.value.decode()
        if name == "uin_str1":
            res["sender"] = int(value)
        elif name == "uin_str2":
            res["target"] = int(value)
        elif name == "suffix_str":
            res["suffix"] = value
        elif name == "action_str":
            res["action"] = value
    if not res["target"]:
        res["target"] = default
    return res


# OnlinePush.ReqPush
async def handle_req_push(
    client: "Client", packet: IncomingPacket
) -> SvcReqPushCommand:
    """Handle Request Push Command.

    Note:
        Source: com.tencent.imcore.message.OnLinePushMessageProcessor.ProcessOneMsg.a
    """
    push = SvcReqPushCommand.decode_response(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
    )

    if isinstance(push, SvcReqPush):
        seq = client.next_seq()
        pkg = encode_push_response(
            seq,
            client._session_id,
            push.message.uin,
            client._siginfo.d2key,
            push.message.svrip,
            [
                DelMsgInfo(
                    from_uin=info.from_uin,
                    msg_seq=info.msg_seq,
                    msg_time=info.msg_time,
                    msg_cookies=info.msg_cookies,
                )
                for info in push.message.msg_info
            ],
            req_id=push.seq,
        )
        await client.send(seq, "OnlinePush.RespPush", pkg)

        for info in push.message.msg_info:
            key = f"{info.msg_seq}" f"{info.msg_time}" f"{info.msg_uid}"
            should_skip = key in client._online_push_cache
            client._online_push_cache[key] = None
            if should_skip:
                continue

            if info.msg_type == 169:
                # handleC2COnlinePushMsgResp
                pass
            elif info.msg_type == 8:
                # HandleShMsgType0x08
                pass
            elif info.msg_type == 132:
                # HandleShMsgType0x84
                pass
            elif info.msg_type == 732:
                content = info.vec_msg
                sub_type = content[4]
                gid = int.from_bytes(content[:4], "big")

                if sub_type in (0x14, 0x11):
                    notify = NotifyMsgBody.FromString(content[7:])
                    if sub_type == 0x14:  # nudge
                        client.dispatch_event(
                            events.NudgeEvent(
                                **_parse_poke(
                                    notify.general_gray_tip.templ_param,
                                    default=info.from_uin,
                                ),
                                group=gid,
                            )
                        )
                    elif sub_type == 0x11:  # recall
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
                elif sub_type == 0x0C:  # mute event
                    operator = int.from_bytes(
                        content[6:10], "big", signed=False
                    )
                    target = int.from_bytes(content[16:20], "big", signed=False)
                    duration = int.from_bytes(
                        content[20:24], "big", signed=False
                    )
                    if duration > 0:  # muted
                        client.dispatch_event(
                            events.MemberMutedEvent(
                                gid, operator, target, duration
                            )
                        )
                    else:
                        client.dispatch_event(
                            events.MemberUnMutedEvent(gid, operator, target)
                        )
            elif info.msg_type == 528:
                # TODO: parse friend event
                pass

    return push


__all__ = [
    "handle_c2c_sync",
    "handle_push_msg",
    "PushMsgCommand",
    "PushMsg",
    "PushMsgError",
]
