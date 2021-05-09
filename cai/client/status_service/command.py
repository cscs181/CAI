"""StatSvc Command Parser.

This module is used to parse StatSvc response packets into command.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional
from dataclasses import dataclass

from cai.client.command import Command
from cai.utils.jce import RequestPacketVersion2, RequestPacketVersion3
from .jce import SvcRespRegister, RequestMSFForceOffline


@dataclass
class SvcRegisterResponse(Command):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "SvcRegisterResponse":
        """Decode StatSvc register response.

        Note:
            Source: com.tencent.mobileqq.servlet.PushServlet.onReceive

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.

        Returns:
            RegisterSuccess: register success.
            RegisterFail: register failed.
        """
        if ret_code != 0 or not data:
            return SvcRegisterResponse(uin, seq, ret_code, command_name)

        try:
            resp_packet = RequestPacketVersion2.decode(data)
            svc_register_response = SvcRespRegister.decode(
                resp_packet.data["SvcRespRegister"][  # type: ignore
                    "QQService.SvcRespRegister"
                ][1:-1]
            )
            return RegisterSuccess(
                uin, seq, ret_code, command_name, svc_register_response
            )
        except Exception as e:
            return RegisterFail(
                uin,
                seq,
                ret_code,
                command_name,
                f"Error when decoding response! {repr(e)}",
            )


@dataclass
class RegisterFail(SvcRegisterResponse):
    message: Optional[str] = None


@dataclass
class RegisterSuccess(SvcRegisterResponse):
    response: SvcRespRegister


@dataclass
class MSFForceOfflineCommand(Command):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "MSFForceOfflineCommand":
        """Decode StatSvc MSF Offline request.

        Note:
            Source: com.tencent.mobileqq.msf.core.af.a

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.
        """
        if ret_code != 0 or not data:
            return MSFForceOfflineCommand(uin, seq, ret_code, command_name)

        try:
            req_packet = RequestPacketVersion3.decode(data)
            msf_offline_request = RequestMSFForceOffline.decode(
                req_packet.data["RequestMSFForceOffline"][1:-1]  # type: ignore
            )
            return MSFForceOffline(
                uin, seq, ret_code, command_name, msf_offline_request
            )
        except Exception as e:
            return MSFForceOfflineError(
                uin,
                seq,
                ret_code,
                command_name,
                f"Error when decoding response! {repr(e)}",
            )


@dataclass
class MSFForceOffline(MSFForceOfflineCommand):
    request: RequestMSFForceOffline


@dataclass
class MSFForceOfflineError(MSFForceOfflineCommand):
    message: str
