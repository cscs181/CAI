import struct
import random
from hashlib import md5

from rtea import qqtea_encrypt


class Tlv:

    # oicq/wlogin_sdk/tlv_type/tlv_t.java
    @classmethod
    def _pack(cls, type: int, data: bytes) -> bytes:
        return struct.pack(">HH", type, len(data)) + data

    @classmethod
    def _pack_lv(cls, data: bytes) -> bytes:
        return struct.pack(">H", len(data)) + data

    @classmethod
    def t1(cls, uin: int, server_time: int, ip: bytes) -> bytes:
        return cls._pack(
            0x1,
            struct.pack(
                ">HIII4sH", 1, random.randint(0, 0xFFFF), uin, server_time, ip,
                0
            )
        )

    @classmethod
    def t2(cls, result: str, sign: bytes) -> bytes:
        return cls._pack(
            0x2,
            struct.pack(">H", 0) + cls._pack_lv(result.encode()) +
            cls._pack_lv(sign)
        )

    @classmethod
    def t8(cls, localId: int) -> bytes:
        return cls._pack(0x8, struct.pack(">HIH", 0, localId, 0))

    @classmethod
    def t18(cls, app_id: int, uin: int) -> bytes:
        return cls._pack(
            0x18, struct.pack(">HIIIIHH", 1, 1536, app_id, 0, uin, 0, 0)
        )

    @classmethod
    def t100(cls, sso_version: int, protocol: int, sigmap: int) -> bytes:
        return cls._pack(
            0x100,
            struct.pack(">HIIIII", 1, sso_version, 16, protocol, 0, sigmap)
        )

    @classmethod
    def t104(cls, data: bytes) -> bytes:
        return cls._pack(0x104, data)

    @classmethod
    def t106(
        cls, uin: int, salt: int, app_id: int, sso_version: int,
        password_md5: bytes, guid_available: bool, guid: bytes,
        tgtgt_key: bytes, wtf: int
    ) -> bytes:
        # TODO
        key = md5(password_md5 + bytes(4) +
                  struct.pack(">I", salt or uin)).digest()
        body = struct.pack(f">HIIIIQI4sc16s{len(tgtgt_key)}sI?")
        data = qqtea_encrypt(body, key)
        return cls._pack(0x106, data)
