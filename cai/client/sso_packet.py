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
        body: Union[bytes, Packet],
        extra_data: Optional[Union[bytes, Packet]] = None
    ) -> "SsoPacket":
        return cls().write(struct.pack(">III", seq, sub_app_id, sub_app_id))
