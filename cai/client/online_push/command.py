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
from cai.utils.jce import RequestPacketVersion2

from .jce import SvcReqPushMsg


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


@dataclass
class SvcReqPushCommand(Command):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "SvcReqPushCommand":
        """Decode OnlinePush request push packet.

        Note:
            Source: com.tencent.mobileqq.service.message.MessageFactoryReceiver.l

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.
        """
        if ret_code != 0 or not data:
            return SvcReqPushCommand(uin, seq, ret_code, command_name)

        try:
            req_packet = RequestPacketVersion2.decode(data)
            svc_req_push = SvcReqPushMsg.decode(
                req_packet.data["req"][  # type: ignore
                    "OnlinePushPack.SvcReqPushMsg"
                ][1:-1]
            )
            return SvcReqPush(uin, seq, ret_code, command_name, svc_req_push)
        except Exception as e:
            return SvcReqPushError(
                uin,
                seq,
                ret_code,
                command_name,
                f"Error when decoding response! {repr(e)}",
            )


@dataclass
class SvcReqPush(SvcReqPushCommand):
    message: SvcReqPushMsg


@dataclass
class SvcReqPushError(SvcReqPushCommand):
    message: str
