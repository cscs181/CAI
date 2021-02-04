import time
import struct
import random
from hashlib import md5
from typing import List, Union

from rtea import qqtea_encrypt


class Packet(bytearray):

    def write(self, *data: Union[bytes, "Packet"]) -> "Packet":
        for i in data:
            self.extend(i)
        return self


class Tlv:

    # oicq/wlogin_sdk/tlv_type/tlv_t.java
    @classmethod
    def _pack_lv(cls, *data: Union[bytes, Packet]) -> Packet:
        return Packet(struct.pack(">H", sum(map(len, data)))).write(*data)

    @classmethod
    def _pack_tlv(cls, type: int, *data: Union[bytes, Packet]) -> Packet:
        return Packet(struct.pack(">HH", type, sum(map(len,
                                                       data)))).write(*data)

    @classmethod
    def _pack_lv_limited(cls, data: Union[bytes, Packet], size: int) -> Packet:
        return cls._pack_lv(data[:size])

    @classmethod
    def _random_int16(cls) -> int:
        return random.randint(0, 0xFFFF)

    @classmethod
    def _random_int32(cls) -> int:
        return random.randint(0, 0xFFFFFFFF)

    @classmethod
    def t1(cls, uin: int, server_time: int, ip: bytes) -> Packet:
        return cls._pack_tlv(
            0x1,
            struct.pack(
                ">HIII4sH", 1, cls._random_int16(), uin, server_time, ip, 0
            )
        )

    @classmethod
    def t2(cls, result: bytes, sign: bytes) -> Packet:
        return cls._pack_tlv(
            0x2, struct.pack(">H", 0), cls._pack_lv(result), cls._pack_lv(sign)
        )

    @classmethod
    def t8(cls, i: int, localId: int, i2: int) -> Packet:
        return cls._pack_tlv(0x8, struct.pack(">HIH", i, localId, i2))

    @classmethod
    def t18(cls, app_id: int, i: int, uin: int, i2: int) -> Packet:
        return cls._pack_tlv(
            0x18, struct.pack(">HIIIIHH", 1, 1536, app_id, i, uin, i2, 0)
        )

    @classmethod
    def t100(
        cls, sso_version: int, j: int, protocol: int, i: int, sigmap: int
    ) -> Packet:
        return cls._pack_tlv(
            0x100,
            struct.pack(">HIIIII", 1, sso_version, j, protocol, i, sigmap)
        )

    @classmethod
    def t104(cls, data: bytes) -> Packet:
        return cls._pack_tlv(0x104, data)

    @classmethod
    def t106(
        cls, sso_version: int, app_id: int, app_client_version: int, uin: int,
        salt: int, ip: bytes, password_md5: bytes, guid_available: bool,
        guid: bytes, tgtgt_key: bytes, wtf: int
    ) -> Packet:
        key = md5(
            Packet().write(
                password_md5, bytes(4), struct.pack(">I", salt or uin)
            )
        ).digest()

        body = Packet().write(
            struct.pack(
                ">HIIIIQ", 4, cls._random_int32(), sso_version, app_id,
                app_client_version, uin or salt
            ),
            struct.pack(
                ">I4sc16s", int(time.time() * 1000), ip, 1, password_md5
            ),
            tgtgt_key,
            struct.pack(">I?", wtf, guid_available),
            guid or struct.pack(
                ">IIII", cls._random_int32(), cls._random_int32(),
                cls._random_int32(), cls._random_int32()
            ),
            struct.pack(
                ">II",
                app_id,
                1  # password login
            ),
            cls._pack_lv(str(uin).encode()),
            struct.pack(">H", 0)
        )

        data = qqtea_encrypt(body, key)
        return cls._pack_tlv(0x106, data)

    @classmethod
    def t107(cls, pic_type: int) -> Packet:
        return cls._pack_tlv(0x107, struct.pack(">HcHc", pic_type, 0, 0, 1))

    @classmethod
    def t108(cls, imei: str) -> Packet:
        return cls._pack_tlv(0x108, imei.encode())

    @classmethod
    def t109(cls, android_id: bytes) -> Packet:
        return cls._pack_tlv(0x109, md5(android_id).digest())

    @classmethod
    def t10a(cls, arr: bytes) -> Packet:
        return cls._pack_tlv(0x10A, arr)

    @classmethod
    def t116(cls, bitmap: int, sub_sigmap: int) -> Packet:
        return cls._pack_tlv(
            0x116, struct.pack(">cIIcI", 0, bitmap, sub_sigmap, 1, 1600000226)
        )

    @classmethod
    def t124(
        cls, os_type: bytes, os_version: bytes, sim_info: bytes, apn: bytes
    ) -> Packet:
        return cls._pack_tlv(
            0x124, cls._pack_lv_limited(os_type, 16),
            cls._pack_lv_limited(os_version, 16), struct.pack(">H", 2),
            cls._pack_lv_limited(sim_info, 16),
            cls._pack_lv_limited(bytes(0), 16), cls._pack_lv_limited(apn, 16)
        )

    @classmethod
    def t128(
        cls, is_guid_from_file_null: bool, is_guid_available: bool,
        is_guid_changed: bool, guid_flag: int, build_model: bytes, guid: bytes,
        build_brand: bytes
    ) -> Packet:
        return cls._pack_tlv(
            0x128,
            struct.pack(
                ">H???I", 0, is_guid_from_file_null, is_guid_available,
                is_guid_changed, guid_flag
            ), cls._pack_lv_limited(build_model, 32),
            cls._pack_lv_limited(guid, 16),
            cls._pack_lv_limited(build_brand, 16)
        )

    @classmethod
    def t141(cls, sim_info: bytes, apn: bytes) -> Packet:
        return cls._pack_tlv(
            0x141, struct.pack(">H", 1), cls._pack_lv(sim_info),
            struct.pack(">H", 2), cls._pack_lv(apn)
        )

    @classmethod
    def t142(cls, apk_id: str) -> Packet:
        return cls._pack_tlv(
            0x142, struct.pack(">H", 0),
            cls._pack_lv_limited(apk_id.encode(), 32)
        )

    @classmethod
    def t143(cls, arr: bytes) -> Packet:
        return cls._pack_tlv(0x143, arr)

    @classmethod
    def t144(
        cls, imei: bytes, dev_info: bytes, os_type: bytes, os_version: bytes,
        sim_info: bytes, apn: bytes, is_guid_from_file_null: bool,
        is_guid_available: bool, is_guid_changed: bool, guid_flag: int,
        build_model: bytes, guid: bytes, build_brand: bytes, tgtgt_key: bytes
    ) -> Packet:
        return cls._pack_tlv(
            0x144,
            qqtea_encrypt(
                Packet().write(
                    struct.pack(">H", 5), cls.t109(imei), cls.t52d(dev_info),
                    cls.t124(os_type, os_version, sim_info, apn),
                    cls.t128(
                        is_guid_from_file_null, is_guid_available,
                        is_guid_changed, guid_flag, build_model, guid,
                        build_brand
                    ), cls.t16e(build_model)
                ), tgtgt_key
            )
        )

    @classmethod
    def t145(cls, guid: bytes) -> Packet:
        return cls._pack_tlv(0x145, guid)

    @classmethod
    def t147(
        cls, app_id: bytes, apk_version_name: bytes, apk_signature_md5: bytes
    ) -> Packet:
        return cls._pack_tlv(
            0x147, struct.pack(">I", app_id),
            cls._pack_lv_limited(apk_version_name, 32),
            cls._pack_lv_limited(apk_signature_md5, 32)
        )

    @classmethod
    def t154(cls, seq: int) -> Packet:
        return cls._pack_tlv(0x154, struct.pack(">I", seq))

    @classmethod
    def t166(cls, image_type: bytes) -> Packet:
        return cls._pack_tlv(0x166, struct.pack(">c", image_type))

    @classmethod
    def t16a(cls, arr: bytes) -> Packet:
        return cls._pack_tlv(0x16A, arr)

    @classmethod
    def t16e(cls, build_model: bytes) -> Packet:
        return cls._pack_tlv(0x16E, build_model)

    @classmethod
    def t174(cls, data: bytes) -> Packet:
        return cls._pack_tlv(0x174, data)

    @classmethod
    def t177(cls, build_time: int, sdk_version: str) -> Packet:
        return cls._pack_tlv(
            0x177, struct.pack(">cI", 1, build_time),
            cls._pack_lv(sdk_version.encode())
        )

    @classmethod
    def t17a(cls, value: int) -> Packet:
        return cls._pack_tlv(0x17A, struct.pack(">I", value))

    @classmethod
    def t17c(cls, code: str) -> Packet:
        return cls._pack_tlv(0x17C, code.encode())

    @classmethod
    def t187(cls, mac_address: bytes) -> Packet:
        return cls._pack_tlv(0x187, md5(mac_address).digest())

    @classmethod
    def t188(cls, android_id: bytes) -> Packet:
        return cls._pack_tlv(0x188, md5(android_id).digest())

    @classmethod
    def t191(cls, k: bytes) -> Packet:
        return cls._pack_tlv(0x191, struct.pack(">c", k))

    @classmethod
    def t193(cls, ticket: str) -> Packet:
        return cls._pack_tlv(0x193, ticket.encode())

    @classmethod
    def t194(cls, imsi_md5: bytes) -> Packet:
        return cls._pack_tlv(0x194, imsi_md5)

    @classmethod
    def t197(cls) -> Packet:
        return cls._pack_tlv(0x197, bytes(1))

    @classmethod
    def t198(cls) -> Packet:
        return cls._pack_tlv(0x198, bytes(1))

    @classmethod
    def t202(cls, wifi_bssid: bytes, wifi_ssid: bytes) -> Packet:
        return cls._pack_tlv(
            0x202, cls._pack_lv_limited(wifi_bssid, 16),
            cls._pack_lv_limited(wifi_ssid, 32)
        )

    @classmethod
    def t400(
        cls, g: bytes, uin: int, guid: bytes, dpwd: bytes, j2: int, j3: int,
        rand_seed: bytes
    ) -> Packet:
        data = Packet().write(
            struct.pack(">HQ", 1, uin), guid, dpwd,
            struct.pack(">III", j2, j3, int(time.time())), rand_seed
        )
        return cls._pack_tlv(0x400, qqtea_encrypt(data, g))

    @classmethod
    def t401(cls, d: bytes) -> Packet:
        return cls._pack_tlv(0x401, d)

    @classmethod
    def t511(cls, domains: List[str]) -> Packet:
        _domains = [domain for domain in domains if domain]

        data: List[bytes] = []
        for domain in _domains:
            index1 = domain.index("(")
            index2 = domain.index(")")
            if index1 != 0 or index2 <= 0:
                data.append(bytes([1]))
                data.append(domain.encode())
            else:
                try:
                    i = int(domain[index1 + 1:index2])
                    data.append(
                        struct.pack(
                            ">B",
                            (((i & 134217728) > 0) << 1) | (1048576 & i) > 0
                        )
                    )
                    data.append(domain[index2 + 1:].encode())
                except Exception:
                    pass
        return cls._pack_tlv(0x511, struct.pack(">H", len(_domains)), *data)

    @classmethod
    def t516(cls) -> Packet:
        return cls._pack_tlv(0x516, struct.pack(">I", 0))

    @classmethod
    def t521(cls) -> Packet:
        return cls._pack_tlv(0x521, struct.pack(">IH", 0, 0))

    @classmethod
    def t525(cls, t536: bytes) -> Packet:
        return cls._pack_tlv(0x525, struct.pack(">H", 1), t536)

    @classmethod
    def t52d(cls, dev_info: bytes) -> Packet:
        return cls._pack_tlv(0x52D, dev_info)

    @classmethod
    def t536(cls, login_extra_data: bytes) -> Packet:
        return cls._pack_tlv(0x536, login_extra_data)
