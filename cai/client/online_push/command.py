"""MessageSvc Command Parser.

This module is used to parse MessageSvc response packets into command.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from dataclasses import dataclass

from cai.client.command import Command
from cai.pb.msf.msg.onlinepush import PbPushMsg
from cai.pb.msf.msg.svc import PbGetGroupMsgResp


# @dataclass
# class GetMessageCommand(Command):
#     @classmethod
#     def decode_response(
#         cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
#     ) -> "GetMessageCommand":
#         """Decode MessageSvc get message response packet.

#         Note:
#             Source: c2c 1002

#             com.tencent.mobileqq.app.handler.receivesuccess.MessageSvcPbGetMsg

#             com.tencent.mobileqq.app.MessageHandler.h

#             com.tencent.imcore.message.C2CMessageProcessor.b

#         Args:
#             uin (int): User QQ
#             seq (int): Sequence number of the response packet.
#             ret_code (int): Return code of the response.
#             command_name (str): Command name of the response.
#             data (bytes): Payload data of the response.
#         """
#         if ret_code != 0 or not data:
#             return GetMessageCommand(uin, seq, ret_code, command_name)

#         try:
#             result = PbGetMsgResp.FromString(data)
#             return GetMessageSuccess(uin, seq, ret_code, command_name, result)
#         except Exception as e:
#             return GetMessageFail(
#                 uin,
#                 seq,
#                 ret_code,
#                 command_name,
#                 f"Error when decoding response! {repr(e)}",
#             )


# @dataclass
# class GetMessageSuccess(GetMessageCommand):
#     response: PbGetMsgResp


# @dataclass
# class GetMessageFail(GetMessageCommand):
#     message: str


@dataclass
class PushMsgCommand(Command):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "PushMsgCommand":
        """Decode OnlinePush push message packet.

        Including commands: ``OnlinePush.PbPushGroupMsg``,
        ``OnlinePush.PbPushDisMsg``, ``OnlinePush.PbC2CMsgSync``,
        ``OnlinePush.PbPushC2CMsg``, ``OnlinePush.PbPushBindUinGroupMsg``

        Note:
            Source: com.tencent.mobileqq.app.MessageHandler.b

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.
        """
        if ret_code != 0 or not data:
            return PushMsgCommand(uin, seq, ret_code, command_name)

        try:
            push_message = PbPushMsg.FromString(data)
            return PushMsg(uin, seq, ret_code, command_name, push_message)
        except Exception as e:
            return PushMsgError(
                uin,
                seq,
                ret_code,
                command_name,
                f"Error when decoding response! {repr(e)}",
            )


@dataclass
class PushMsg(PushMsgCommand):
    push: PbPushMsg


@dataclass
class PushMsgError(PushMsgCommand):
    message: str
