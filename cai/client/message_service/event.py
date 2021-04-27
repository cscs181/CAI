"""MessageSvc Event Parser.

This module is used to parse MessageSvc response packets into event.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional
from dataclasses import dataclass

from cai.client.event import Event
from .jce import RequestPushForceOffline
from cai.utils.jce import RequestPacketVersion2


@dataclass
class PushForceOfflineEvent(Event):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "PushForceOfflineEvent":
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
            return PushForceOfflineEvent(uin, seq, ret_code, command_name)

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
class PushForceOffline(PushForceOfflineEvent):
    request: RequestPushForceOffline


@dataclass
class PushForceOfflineError(PushForceOfflineEvent):
    message: str
