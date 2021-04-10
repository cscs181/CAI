"""StatSvc Event Parser.

This module is used to parse StatSvc response packets into event.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Union, Optional
from dataclasses import dataclass

from .jce import SvcRespRegister
from cai.client.event import Event
from cai.utils.jce import RequestPacketVersion3


@dataclass
class SvcRegisterResponse(Event):
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
            resp_packet = RequestPacketVersion3.decode(data)
            svc_register_response = SvcRespRegister.decode(
                resp_packet.data["SvcRespRegister"][
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
