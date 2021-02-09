"""

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import struct
from typing import Union, Optional

from cai.utils.binary import Packet


class SsoPacket(Packet):

    @classmethod
    def build(
        cls,
        seq: int,
        sub_app_id: int,
        command_name: str,
        imei: str,
        session_id: bytes,
        ksid: bytes,
        body: Union[bytes, Packet],
        extra_data: Optional[Union[bytes, Packet]] = None,
        unknown_bytes: bytes = bytes(
            [
                0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x01, 0x00
            ]
        )
    ) -> "SsoPacket":
        extra = extra_data and (len(extra_data) != 4)
        return cls().write(
            struct.pack(">III", seq, sub_app_id, sub_app_id), unknown_bytes,
            struct.pack(">I", 4) if not extra else b"",
            struct.pack(">I",
                        len(extra_data) + 4) if extra_data and extra else b"",
            extra_data if extra_data and extra else b"",
            struct.pack(">I",
                        len(command_name) + 4), command_name.encode(),
            struct.pack(">I",
                        len(session_id) + 4), session_id,
            struct.pack(">I",
                        len(imei) + 4), imei.encode(),
            struct.pack(">IH", 4,
                        len(ksid) + 2), ksid, struct.pack(">I", 4)
        )
