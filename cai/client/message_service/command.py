"""MessageSvc Command Parser.

This module is used to parse MessageSvc response packets into command.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from dataclasses import dataclass

from cai.client.command import Command
from cai.pb.msf.msg.svc import PbGetMsgResp
from cai.utils.jce import RequestPacketVersion2

from .jce import RequestPushNotify, RequestPushForceOffline


@dataclass
class GetMessageCommand(Command):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "GetMessageCommand":
        """Decode MessageSvc get message response packet.

        Note:
            Source: c2c 1002

            com.tencent.mobileqq.app.handler.receivesuccess.MessageSvcPbGetMsg

            com.tencent.mobileqq.app.MessageHandler.h

            com.tencent.imcore.message.C2CMessageProcessor.b

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.
        """
        if ret_code != 0 or not data:
            return GetMessageCommand(uin, seq, ret_code, command_name)

        try:
            result = PbGetMsgResp.FromString(data)
            return GetMessageSuccess(uin, seq, ret_code, command_name, result)
        except Exception as e:
            return GetMessageFail(
                uin,
                seq,
                ret_code,
                command_name,
                f"Error when decoding response! {repr(e)}",
            )


@dataclass
class GetMessageSuccess(GetMessageCommand):
    response: PbGetMsgResp


@dataclass
class GetMessageFail(GetMessageCommand):
    message: str


@dataclass
class PushNotifyCommand(Command):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "PushNotifyCommand":
        """Decode MessageSvc push notify packet.

        Note:
            Source: com.tencent.mobileqq.service.message.MessageFactoryReceiver.f

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.
        """
        if ret_code != 0 or not data:
            return PushNotifyCommand(uin, seq, ret_code, command_name)

        try:
            # data offset 4 in source? test get 15
            # req_packet = RequestPacketVersion2.decode(data[4:])
            req_packet = RequestPacketVersion2.decode(data[15:])
            push_offline_request = RequestPushNotify.decode(
                req_packet.data["req_PushNotify"][  # type: ignore
                    "PushNotifyPack.RequestPushNotify"
                ][1:-1]
            )
            return PushNotify(
                uin, seq, ret_code, command_name, push_offline_request
            )
        except Exception as e:
            return PushNotifyError(
                uin,
                seq,
                ret_code,
                command_name,
                f"Error when decoding response! {repr(e)}",
            )


@dataclass
class PushNotify(PushNotifyCommand):
    notify: RequestPushNotify


@dataclass
class PushNotifyError(PushNotifyCommand):
    message: str


@dataclass
class PushForceOfflineCommand(Command):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "PushForceOfflineCommand":
        """Decode MessageSvc Force Offline request.

        Note:
            Source: mqq.app.MainService

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.
        """
        if ret_code != 0 or not data:
            return PushForceOfflineCommand(uin, seq, ret_code, command_name)

        try:
            req_packet = RequestPacketVersion2.decode(data)
            push_offline_request = RequestPushForceOffline.decode(
                req_packet.data["req_PushForceOffline"][  # type: ignore
                    "PushNotifyPack.RequestPushForceOffline"
                ][1:-1]
            )
            return PushForceOffline(
                uin, seq, ret_code, command_name, push_offline_request
            )
        except Exception as e:
            return PushForceOfflineError(
                uin,
                seq,
                ret_code,
                command_name,
                f"Error when decoding response! {repr(e)}",
            )


@dataclass
class PushForceOffline(PushForceOfflineCommand):
    request: RequestPushForceOffline


@dataclass
class PushForceOfflineError(PushForceOfflineCommand):
    message: str
