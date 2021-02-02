import time
import struct
import random


class Tlv:

    # oicq/wlogin_sdk/tlv_type/tlv_t.java
    @classmethod
    def _pack(cls, type: int, data: bytes) -> bytes:
        return struct.pack(">HH", type, len(data)) + data

    # oicq/wlogin_sdk/tlv_type/tlv_t1.java
    @classmethod
    def t1(cls, qq: int, server_time: int, ip: bytes) -> bytes:
        return cls._pack(
            0x1,
            struct.pack(
                ">HIII4sH", 1, random.randint(0, 0xFFFF), qq, server_time, ip, 0
            )
        )

    # oicq/wlogin_sdk/tlv_type/tlv_t18.java
    @classmethod
    def t18(cls, app_id: int, qq: int) -> bytes:
        return cls._pack(
            0x18, struct.pack(">HIIIIHH", 1, 1536, app_id, 0, qq, 0, 0)
        )
