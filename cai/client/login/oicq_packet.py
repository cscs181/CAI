"""OICQ Packet Builder

This module is used to build and handle OICQ packets.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import struct
from typing import Type, Union

from cai.utils.binary import Packet


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
