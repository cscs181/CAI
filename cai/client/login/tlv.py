"""TLV Tools

This module is used to build and handle tlv bytes.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import time
import struct
import random
from hashlib import md5
from typing import Any, List, Dict, Union

from rtea import qqtea_encrypt, qqtea_decrypt

from cai.log import logger
from .data_pb2 import DeviceInfo
from cai.utils.binary import Packet
from cai.settings.device import get_device

DEVICE = get_device()


class TlvEncoder:

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
    def t8(cls, local_id: int, i: int = 0, i2: int = 0) -> Packet:
        return cls._pack_tlv(0x8, struct.pack(">HIH", i, local_id, i2))

    @classmethod
    def t18(
        cls,
        app_id: int,
        app_client_version: int,
        uin: int,
        unknown: int = 0
    ) -> Packet:
        return cls._pack_tlv(
            0x18,
            struct.pack(
                ">HIIIIHH", 1, 1536, app_id, app_client_version, uin, unknown, 0
            )
        )

    @classmethod
    def t100(
        cls, sso_version: int, app_id: int, sub_app_id: int,
        app_client_version: int, sigmap: int
    ) -> Packet:
        return cls._pack_tlv(
            0x100,
            struct.pack(
                ">HIIIII", 1, sso_version, app_id, sub_app_id,
                app_client_version, sigmap
            )
        )

    @classmethod
    def t104(cls, data: bytes) -> Packet:
        return cls._pack_tlv(0x104, data)

    @classmethod
    def t106(
        cls, sso_version: int, app_id: int, sub_app_id: int,
        app_client_version: int, uin: int, salt: int, ip: bytes,
        password_md5: bytes, guid_available: bool, guid: bytes, tgtgt_key: bytes
    ) -> Packet:
        key = md5(
            Packet.build(
                password_md5, bytes(4), struct.pack(">I", salt or uin)
            )
        ).digest()

        body = Packet.build(
            struct.pack(
                ">HIIIIQ",
                4,  # tgtgt version
                cls._random_int32(),
                sso_version,
                app_id,
                app_client_version,
                uin or salt
            ),
            struct.pack(">I", int(time.time() * 1000)),
            ip,
            struct.pack(">B", 1),  # save password,
            struct.pack(">16s", password_md5),
            tgtgt_key,
            struct.pack(">I?", 0, guid_available),
            guid or struct.pack(
                ">IIII", cls._random_int32(), cls._random_int32(),
                cls._random_int32(), cls._random_int32()
            ),
            struct.pack(
                ">II",
                sub_app_id,
                1  # password login
            ),
            cls._pack_lv(str(uin).encode()),
            # struct.pack(">H", 0)  # not found in source
        )

        data = qqtea_encrypt(body, key)
        return cls._pack_tlv(0x106, data)

    @classmethod
    def t107(
        cls,
        pic_type: int = 0,
        i1: int = 0,
        i2: int = 0,
        i3: int = 1
    ) -> Packet:
        return cls._pack_tlv(0x107, struct.pack(">HBHB", pic_type, i1, i2, i3))

    @classmethod
    def t108(cls, ksid: str) -> Packet:
        return cls._pack_tlv(0x108, ksid.encode())

    @classmethod
    def t109(cls, android_id: bytes) -> Packet:
        return cls._pack_tlv(0x109, md5(android_id).digest())

    @classmethod
    def t10a(cls, arr: bytes) -> Packet:
        return cls._pack_tlv(0x10A, arr)

    @classmethod
    def t116(
        cls,
        bitmap: int,
        sub_sigmap: int,
        sub_app_id_list: List[int] = [1600000226]
    ) -> Packet:
        return cls._pack_tlv(
            0x116,
            struct.pack(">BIIB", 0, bitmap, sub_sigmap, len(sub_app_id_list)),
            *[struct.pack(">I", id) for id in sub_app_id_list]
        )

    @classmethod
    def t124(
        cls, os_type: bytes, os_version: bytes, network_type: int,
        sim_info: bytes, apn: bytes
    ) -> Packet:
        return cls._pack_tlv(
            0x124, cls._pack_lv_limited(os_type, 16),
            cls._pack_lv_limited(os_version, 16),
            struct.pack(">H", network_type), cls._pack_lv_limited(sim_info, 16),
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
    def t141(cls, sim_info: bytes, network_type: int, apn: bytes) -> Packet:
        return cls._pack_tlv(
            0x141, struct.pack(">H", 1), cls._pack_lv(sim_info),
            struct.pack(">H", network_type), cls._pack_lv(apn)
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
        cls, imei: bytes, bootloader: str, proc_version: str, codename: str,
        incremental: str, fingerprint: str, boot_id: str, android_id: str,
        baseband: str, inner_version: str, os_type: bytes, os_version: bytes,
        network_type: int, sim_info: bytes, apn: bytes,
        is_guid_from_file_null: bool, is_guid_available: bool,
        is_guid_changed: bool, guid_flag: int, build_model: bytes, guid: bytes,
        build_brand: bytes, tgtgt_key: bytes
    ) -> Packet:
        return cls._pack_tlv(
            0x144,
            qqtea_encrypt(
                Packet.build(
                    struct.pack(">H", 5), cls.t109(imei),
                    cls.t52d(
                        bootloader, proc_version, codename, incremental,
                        fingerprint, boot_id, android_id, baseband,
                        inner_version
                    ),
                    cls.t124(os_type, os_version, network_type, sim_info, apn),
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
        cls, app_id: int, apk_version_name: bytes, apk_signature_md5: bytes
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
            0x177, struct.pack(">BI", 1, build_time),
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
    def t191(cls, k: int) -> Packet:
        return cls._pack_tlv(0x191, struct.pack(">B", k))

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
        data = Packet.build(
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
                            (((i & 134217728) > 0) << 1) | ((1048576 & i) > 0)
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
    def t521(cls, product_type: int = 0) -> Packet:
        return cls._pack_tlv(0x521, struct.pack(">IH", product_type, 0))

    @classmethod
    def t525(cls, t536: Packet) -> Packet:
        return cls._pack_tlv(0x525, struct.pack(">H", 1), t536)

    @classmethod
    def t52d(
        cls, bootloader: str, proc_version: str, codename: str,
        incremental: str, fingerprint: str, boot_id: str, android_id: str,
        baseband: str, inner_version: str
    ) -> Packet:
        device_info = DeviceInfo(
            bootloader=bootloader,
            proc_version=proc_version,
            codename=codename,
            incremental=incremental,
            fingerprint=fingerprint,
            boot_id=boot_id,
            android_id=android_id,
            base_band=baseband,
            inner_version=inner_version
        )
        return cls._pack_tlv(0x52D, device_info.SerializeToString())

    @classmethod
    def t536(cls, login_extra_data: bytes) -> Packet:
        return cls._pack_tlv(0x536, login_extra_data)


class TlvDecoder:

    @classmethod
    def decode(
        cls,
        data: Union[bytes, Packet],
        offset: int = 0,
        tag_size: int = 2
    ) -> Dict[int, Any]:
        if not isinstance(data, Packet):
            data = Packet(data)

        result: Dict[int, bytes] = {}
        while offset + tag_size <= len(data):
            tag: int
            if tag_size == 1:
                tag = data.read_int8(offset)
                offset += 1
            elif tag_size == 2:
                tag = data.read_int16(offset)
                offset += 2
            elif tag_size == 4:
                tag = data.read_int32(offset)
                offset += 4
            else:
                raise ValueError(
                    f"Invalid tag size. Expected 1 / 2 / 4, got {tag_size}."
                )

            if tag == 255:
                return result

            length = data.read_uint16(offset)
            offset += 2
            value = data.read_bytes(length, offset)
            futher_decode = getattr(cls, f"t{tag:x}", None)
            if futher_decode:
                value = futher_decode(cls, value)
            result[tag] = value

        return result

    @classmethod
    def t108(cls, data: bytes) -> Dict[str, Any]:
        return {"ksid": data}

    @classmethod
    def t113(cls, data: bytes) -> Dict[str, Any]:
        return {"uin": struct.unpack_from(">I", data)[0]}

    @classmethod
    def t119(cls, data: bytes) -> Dict[int, Any]:
        data = qqtea_decrypt(data, DEVICE.tgtgt)
        result = cls.decode(data, offset=2)
        return result

    @classmethod
    def t11a(cls, data: bytes) -> Dict[str, Any]:
        data_ = Packet(data)
        return {
            "age": data_.read_uint8(2),
            "gender": data_.read_uint8(3),
            "nick": data_.read_bytes(data_.read_uint8(4), 5).decode()
        }

    @classmethod
    def t125(cls, data: bytes) -> Dict[str, Any]:
        data_ = Packet(data)
        offset = 0
        id_length = data_.read_uint16(offset)
        offset += 2 + id_length
        key_length = data_.read_uint16(offset)
        return {
            "open_id": data_.read_bytes(id_length, 2),
            "open_key": data_.read_bytes(key_length, offset + 2)
        }

    @classmethod
    def t130(cls, data: bytes) -> Dict[str, Any]:
        data_ = Packet(data)
        return {"time_diff": data_.read_int32(), "t149": data_.read_bytes(4)}

    # @classmethod
    # def t138(cls, data: bytes) -> Dict[str, Any]:
    #     return {}

    @classmethod
    def t161(cls, data: bytes) -> Dict[int, bytes]:
        result = cls.decode(data, offset=2)
        return result

    @classmethod
    def t172(cls, data: bytes) -> Dict[str, bytes]:
        return {"rollback_sig": data}

    @classmethod
    def t186(cls, data: bytes) -> Dict[str, Any]:
        return {"pwd_flag": data[0] == bytes([1])}

    @classmethod
    def t199(cls, data: bytes) -> Dict[str, Any]:
        data_ = Packet(data)
        offset = 0
        id_length = data_.read_uint16(offset)
        offset += 2 + id_length
        token_length = data_.read_uint16(offset)
        return {
            "open_id": data_.read_bytes(id_length, 2),
            "pay_token": data_.read_bytes(token_length, offset + 2)
        }

    @classmethod
    def t200(cls, data: bytes) -> Dict[str, Any]:
        data_ = Packet(data)
        offset = 0
        pf_length = data_.read_uint16(offset)
        offset += 2 + pf_length
        key_length = data_.read_uint16(offset)
        return {
            "pf": data_.read_bytes(pf_length, 2),
            "pf_key": data_.read_bytes(key_length, offset + 2)
        }

    @classmethod
    def t512(cls, data: bytes) -> Dict[str, Any]:
        data_ = Packet(data)
        offset = 0
        length = data_.read_uint16()
        offset += 2

        ps_key_map: Dict[str, bytes] = {}
        ps4_token_map: Dict[str, bytes] = {}
        for i in range(length):
            domain_length = data_.read_uint16(offset)
            offset += 2
            domain = data_.read_bytes(domain_length, offset).decode()
            offset += domain_length

            key_length = data_.read_uint16(offset)
            offset += 2
            ps_key = data_.read_bytes(key_length, offset)
            offset += key_length

            token_length = data_.read_uint16(offset)
            offset += 2
            ps4_token = data_.read_bytes(token_length, offset)
            offset += token_length

            ps_key_map[domain] = ps_key
            ps4_token_map[domain] = ps4_token

        return {"ps_key_map": ps_key_map, "ps4_token_map": ps4_token_map}

    @classmethod
    def t531(cls, data: bytes) -> Dict[str, Any]:
        result = cls.decode(data)
        return {
            "a1": (result.get(0x106, b"") + result.get(0x10c, b"")) or None,
            "no_pic_sig": result.get(0x16a)
        }
