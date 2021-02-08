"""OICQ Packet Builder

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import struct

from cai.utils.binary import Packet


class OICQRequest:
    """Build OICQ Request Packet

    Note:
        Source: oicq.wlogin_sdk.request.oicq_request
    """

    @classmethod
    def build(
        cls, uin: int, command_id: int, encoded: bytes, id: int
    ) -> Packet:
        return Packet().write(
            struct.pack(
                ">BHHHHIBBBIII", 2, 27 + 2 + len(encoded), 8001, command_id, 1,
                uin, 3, id, 0, 2, 0, 0
            ), encoded, bytes([3])
        )
