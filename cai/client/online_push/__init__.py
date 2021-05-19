"""OnlinePush Related SDK.

This module is used to build and handle online push related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import List, Union, Optional, TYPE_CHECKING

from cai.utils.binary import Packet
from cai.client.packet import UniPacket, IncomingPacket
from .command import (
    # GetMessageCommand,
    # GetMessageSuccess,
    # GetMessageFail,
    PushMsgCommand,
    PushMsg,
    PushMsgError,
    # PushForceOfflineCommand,
    # PushForceOffline,
    # PushForceOfflineError,
)

if TYPE_CHECKING:
    from cai.client import Client


# def encode_get_message(
#     seq: int,
#     session_id: bytes,
#     uin: int,
#     d2key: bytes,
#     request_type: int,
#     sync_flag: Union[int, SyncFlag] = SyncFlag.START,
#     sync_cookie: Optional[bytes] = None,
#     online_sync_flag: int = 0,
#     pubaccount_cookie: Optional[bytes] = None,
#     server_buf: Optional[bytes] = None,
# ) -> Packet:
#     """Build get message packet.

#     Called in ``com.tencent.mobileqq.app.MessageHandler.a``.

#     command name: ``MessageSvc.PbGetMsg``

#     Note:
#         Source: com.tencent.mobileqq.app.MessageHandler.a

#     Args:
#         seq (int): Packet sequence.
#         session_id (bytes): Session ID.
#         uin (int): User QQ number.
#         d2key (bytes): Siginfo d2 key.
#         request_type (int): Request type.
#         sync_flag (Union[int, SyncFlag], optional): Sync flag.
#             Defaults to :obj:`SyncFlag.START`.
#         sync_cookie (Optional[bytes], optional): Sync cookie. Defaults to None.
#         online_sync_flag (int, optional): Online sync flag. Defaults to 0.
#         pubaccount_cookie (Optional[bytes], optional): Pubaccount cookie.
#             Defaults to None.
#         server_buf (Optional[bytes], optional): Server buf from ``PushNotify``.
#             Defaults to None.

#     Returns:
#         Packet: PbGetMsg packet.
#     """
#     COMMAND_NAME = "MessageSvc.PbGetMsg"

#     # payload = PbGetMsgReq(
#     #     sync_flag=sync_flag,
#     #     sync_cookie=sync_cookie,
#     #     ramble_flag=0,
#     #     latest_ramble_number=20,
#     #     other_ramble_number=3,
#     #     online_sync_flag=online_sync_flag,
#     #     context_flag=1,
#     #     req_type=request_type,
#     #     pubaccount_cookie=pubaccount_cookie,
#     #     server_buf=server_buf,
#     # ).SerializeToString()
#     packet = UniPacket.build(
#         uin, seq, COMMAND_NAME, session_id, 1, payload, d2key
#     )
#     return packet


# async def handle_get_message(
#     client: "Client", packet: IncomingPacket
# ) -> "GetMessageCommand":
#     """Handle Pb Get Message response.

#     Note:
#         Source:

#         com.tencent.imcore.message.C2CMessageProcessor.b

#         com.tencent.imcore.message.C2CMessageProcessor.a

#         com.tencent.imcore.message.C2CMessageProcessorCallback.a

#         com.tencent.imcore.message.DecodeMsg.a
#     """
#     # resp = GetMessageCommand.decode_response(
#     #     packet.uin,
#     #     packet.seq,
#     #     packet.ret_code,
#     #     packet.command_name,
#     #     packet.data,
#     # )
#     # return resp


# def encode_delete_message(
#     seq: int,
#     session_id: bytes,
#     uin: int,
#     d2key: bytes,
#     items: List[PbDeleteMsgReq.MsgItem],
# ) -> Packet:
#     """Build delete message packet.

#     Called in ``com.tencent.mobileqq.app.MessageHandler.a``.

#     command name: ``MessageSvc.PbDeleteMsg``

#     Note:
#         Source: com.tencent.mobileqq.app.MessageHandler.a

#     Args:
#         seq (int): Packet sequence.
#         session_id (bytes): Session ID.
#         uin (int): User QQ number.
#         d2key (bytes): Siginfo d2 key.
#         items (List[PbDeleteMsgReq.MsgItem]): List of message items.

#     Returns:
#         Packet: PbDeleteMsg packet.
#     """
#     COMMAND_NAME = "MessageSvc.PbDeleteMsg"

#     payload = PbDeleteMsgReq(msg_items=items).SerializeToString()
#     packet = UniPacket.build(
#         uin, seq, COMMAND_NAME, session_id, 1, payload, d2key
#     )
#     return packet


async def _handle_c2c_sync(client: "Client", push: PushMsg):
    """Handle C2C Message Sync.

    Note:
        c2c 2003
        Source: com.tencent.imcore.message.C2CMessageProcessor.b
    """
    ...


async def handle_push_msg(
    client: "Client", packet: IncomingPacket
) -> PushMsgCommand:
    """Handle Push Message Command.

    Note:
        Source: com.tencent.mobileqq.app.MessageHandler.b
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
        command_name = push.command_name
        if command_name == "OnlinePush.PbC2CMsgSync":
            await _handle_c2c_sync(client, push)
        elif command_name == "OnlinePush.PbPushBindUinGroupMsg":
            # sub account message
            pass
        elif msg_type == 43 or msg_type == 82:
            # TODO: troop 1001
            pass
        elif msg_type == 141:
            # TODO: c2c 1001
            pass
        elif msg_type != 42:
            # discussion 1001
            pass

    return push


__all__ = [
    "handle_push_msg",
    "PushMsgCommand",
    "PushMsg",
    "PushMsgError",
]
