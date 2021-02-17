"""OICQ Packet Builder

This module is used to build and handle OICQ packets.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import struct
from typing import Dict, Union
from dataclasses import dataclass

from .tlv import TlvDecoder
from cai.utils.binary import Packet
from cai.client.packet import IncomingPacket


class OICQRequest(Packet):
    """Build OICQ Request Packet

    Note:
        Source: oicq.wlogin_sdk.request.oicq_request
    """

    @classmethod
    def build_encoded(
        cls, uin: int, command_id: int, encoded: Union[bytes, Packet],
        encoder_id: int
    ) -> "OICQRequest":
        return cls().write(
            struct.pack(
                ">BHHHHIBBBIII",
                2,
                27 + 2 + len(encoded),
                8001,  # oicq.wlogin_sdk.request.oicq_request.i
                command_id,
                1,
                uin,
                3,
                encoder_id,
                0,  # oicq.wlogin_sdk.request.oicq_request.m
                2,
                0,
                0
            ),
            encoded,
            bytes([3])
        )


@dataclass
class OICQResponse(IncomingPacket):
    sub_command: int
    status: int
    tlv_map: Dict[int, bytes]

    def __init__(
        self, uin: str, seq: int, ret_code: int, extra: bytes,
        command_name: str, session_id: bytes, data: bytes
    ):
        super().__init__(
            uin, seq, ret_code, extra, command_name, session_id, data
        )
        self.parse(data)

    def parse(self, data: Union[bytes, Packet]):
        if not isinstance(data, Packet):
            data = Packet(data)

        offset = 0
        self.sub_command = data.read_uint16(offset)
        offset += 2
        self.status = data.read_uint8(offset)
        offset += 1 + 2

        self.tlv_map = TlvDecoder.decode(data, offset)
