import time
import struct
import random
from hashlib import md5

from rtea import qqtea_encrypt


class Tlv:

    # oicq/wlogin_sdk/tlv_type/tlv_t.java
    @classmethod
    def _pack_lv(cls, data: bytes) -> bytes:
        return struct.pack(">H", len(data)) + data

    @classmethod
    def _pack_tlv(cls, type: int, data: bytes) -> bytes:
        return struct.pack(">HH", type, len(data)) + data

    @classmethod
    def _pack_lv_limited(cls, data: bytes, size: int) -> bytes:
        return cls._pack_lv(data[:size])

    @classmethod
    def _random_int16(cls) -> int:
        return random.randint(0, 0xFFFF)

    @classmethod
    def _random_int32(cls) -> int:
        return random.randint(0, 0xFFFFFFFF)

    @classmethod
    def t1(cls, uin: int, server_time: int, ip: bytes) -> bytes:
        return cls._pack_tlv(
            0x1,
            struct.pack(
                ">HIII4sH", 1, cls._random_int16(), uin, server_time, ip, 0
            )
        )

    @classmethod
    def t2(cls, result: bytes, sign: bytes) -> bytes:
        return cls._pack_tlv(
            0x2,
            struct.pack(">H", 0) + cls._pack_lv(result) + cls._pack_lv(sign)
        )

    @classmethod
    def t8(cls, i: int, localId: int, i2: int) -> bytes:
        return cls._pack_tlv(0x8, struct.pack(">HIH", i, localId, i2))

    @classmethod
    def t18(cls, app_id: int, i: int, uin: int, i2: int) -> bytes:
        return cls._pack_tlv(
            0x18, struct.pack(">HIIIIHH", 1, 1536, app_id, i, uin, i2, 0)
        )

    @classmethod
    def t100(
        cls, sso_version: int, j: int, protocol: int, i: int, sigmap: int
    ) -> bytes:
        return cls._pack_tlv(
            0x100,
            struct.pack(">HIIIII", 1, sso_version, j, protocol, i, sigmap)
        )

    @classmethod
    def t104(cls, data: bytes) -> bytes:
        return cls._pack_tlv(0x104, data)

    @classmethod
    def t106(
        cls, sso_version: int, app_id: int, app_client_version: int, uin: int,
        salt: int, ip: bytes, password_md5: bytes, guid_available: bool,
        guid: bytes, tgtgt_key: bytes, wtf: int
    ) -> bytes:
        key = md5(password_md5 + bytes(4) +
                  struct.pack(">I", salt or uin)).digest()

        body = struct.pack(
            f">HIIIIQI4sc16s", 4, cls._random_int32(),
            sso_version, app_id, app_client_version, uin or salt,
            int(time.time() * 1000), ip, 1, password_md5
        )
        body += tgtgt_key + struct.pack(
            ">I?", wtf, guid_available
        ) + guid or struct.pack(
            ">IIII", cls._random_int32(), cls._random_int32(),
            cls._random_int32(), cls._random_int32()
        ) + struct.pack(
            ">II",
            app_id,
            1  # password login
        ) + cls._pack_lv(str(uin).encode()) + struct.pack(">H", 0)

        data = qqtea_encrypt(body, key)
        return cls._pack_tlv(0x106, data)

    @classmethod
    def t107(cls, pic_type: int) -> bytes:
        return cls._pack_tlv(0x107, struct.pack(">HcHc", pic_type, 0, 0, 1))

    @classmethod
    def t108(cls, imei: str) -> bytes:
        return cls._pack_tlv(0x108, imei.encode())

    @classmethod
    def t109(cls, android_id: bytes) -> bytes:
        return cls._pack_tlv(0x109, md5(android_id).digest())

    @classmethod
    def t10a(cls, arr: bytes) -> bytes:
        return cls._pack_tlv(0x10A, arr)

    @classmethod
    def t116(cls, bitmap: int, sub_sigmap: int) -> bytes:
        return cls._pack_tlv(
            0x116, struct.pack(">cIIcI", 0, bitmap, sub_sigmap, 1, 1600000226)
        )

    @classmethod
    def t124(
        cls, os_type: bytes, os_version: bytes, sim_info: bytes, apn: bytes
    ) -> bytes:
        return cls._pack_tlv(
            0x124,
            cls._pack_lv_limited(os_type, 16) +
            cls._pack_lv_limited(os_version, 16) + struct.pack(">H", 2) +
            cls._pack_lv_limited(sim_info, 16) +
            cls._pack_lv_limited(bytes(0), 16) + cls._pack_lv_limited(apn, 16)
        )

    @classmethod
    def t128(
        cls, is_guid_from_file_null: bool, is_guid_available: bool,
        is_guid_changed: bool, guid_flag: int, build_model: bytes, guid: bytes,
        build_brand: bytes
    ) -> bytes:
        return cls._pack_tlv(
            0x128,
            struct.pack(
                ">H???I", 0, is_guid_from_file_null, is_guid_available,
                is_guid_changed, guid_flag
            ) + cls._pack_lv_limited(build_model, 32) +
            cls._pack_lv_limited(guid, 16) +
            cls._pack_lv_limited(build_brand, 16)
        )

    @classmethod
    def t141(cls, sim_info: bytes, apn: bytes) -> bytes:
        return cls._pack_tlv(
            0x141,
            struct.pack(">H", 1) + cls._pack_lv(sim_info) +
            struct.pack(">H", 2) + cls._pack_lv(apn)
        )

    @classmethod
    def t142(cls, apk_id: str) -> bytes:
        return cls._pack_tlv(
            0x142,
            struct.pack(">H", 0) + cls._pack_lv_limited(apk_id.encode(), 32)
        )

    @classmethod
    def t143(cls, arr: bytes) -> bytes:
        return cls._pack_tlv(0x143, arr)

    @classmethod
    def t144(
        cls, imei: bytes, dev_info: bytes, os_type: bytes, os_version: bytes,
        sim_info: bytes, apn: bytes, is_guid_from_file_null: bool,
        is_guid_available: bool, is_guid_changed: bool, guid_flag: int,
        build_model: bytes, guid: bytes, build_brand: bytes, tgtgt_key: bytes
    ) -> bytes:
        return cls._pack_tlv(
            0x144,
            qqtea_encrypt(
                struct.pack(">H", 5) + cls.t109(imei) + cls.t52d(dev_info) +
                cls.t124(os_type, os_version, sim_info, apn) + cls.t128(
                    is_guid_from_file_null, is_guid_available, is_guid_changed,
                    guid_flag, build_model, guid, build_brand
                ) + cls.t16e(build_model), tgtgt_key
            )
        )

    @classmethod
    def t145(cls, guid: bytes) -> bytes:
        return cls._pack_tlv(0x145, guid)

    @classmethod
    def t147(
        cls, app_id: bytes, apk_version_name: bytes, apk_signature_md5: bytes
    ) -> bytes:
        return cls._pack_tlv(
            0x147,
            struct.pack(">I", app_id) +
            cls._pack_lv_limited(apk_version_name, 32) +
            cls._pack_lv_limited(apk_signature_md5, 32)
        )
