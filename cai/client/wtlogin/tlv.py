"""TLV Tools

This module is used to build and handle tlv bytes.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import time
import struct
import random
from hashlib import md5
from typing import Any, List, Dict, Union

from rtea import qqtea_encrypt, qqtea_decrypt

from cai.settings.device import get_device
from cai.utils.binary import Packet
from cai.pb.wtlogin.data_pb2 import DeviceReport

DEVICE = get_device()


class TlvEncoder:

    # oicq/wlogin_sdk/tlv_type/tlv_t.java
    @classmethod
    def _pack_lv(cls, *data: Union[bytes, "Packet[()]"]) -> "Packet[()]":
        return Packet(struct.pack(">H", sum(map(len, data)))).write(*data)

    @classmethod
    def _pack_tlv(
        cls, type: int, *data: Union[bytes, "Packet[()]"]
    ) -> "Packet[()]":
        return Packet(struct.pack(">HH", type, sum(map(len, data)))).write(
            *data
        )

    @classmethod
    def _pack_lv_limited(
        cls, data: Union[bytes, "Packet[()]"], size: int
    ) -> "Packet[()]":
        return cls._pack_lv(data[:size])

    @classmethod
    def _random_int16(cls) -> int:
        return random.randint(0, 0xFFFF)

    @classmethod
    def _random_int32(cls) -> int:
        return random.randint(0, 0xFFFFFFFF)

    @classmethod
    def t1(
        cls, uin: int, server_time: int, ip: bytes, ip_version: int = 1
    ) -> "Packet[()]":
        return cls._pack_tlv(
            0x1,
            struct.pack(
                ">HIII4sH",
                ip_version,
                cls._random_int32(),
                uin,
                server_time,
                ip,
                0,
            ),
        )

    @classmethod
    def t2(cls, captcha: bytes, sign: bytes) -> "Packet[()]":
        return cls._pack_tlv(
            0x2, struct.pack(">H", 0), cls._pack_lv(captcha), cls._pack_lv(sign)
        )

    @classmethod
    def t8(cls, local_id: int, i: int = 0, i2: int = 0) -> "Packet[()]":
        return cls._pack_tlv(0x8, struct.pack(">HIH", i, local_id, i2))

    @classmethod
    def t18(
        cls,
        app_id: int,
        app_client_version: int,
        uin: int,
        _ping_version: int = 1,
        _sso_version: int = 1536,
        unknown: int = 0,
    ) -> "Packet[()]":
        return cls._pack_tlv(
            0x18,
            struct.pack(
                ">HIIIIHH",
                _ping_version,
                _sso_version,
                app_id,
                app_client_version,
                uin,
                unknown,
                0,
            ),
        )

    @classmethod
    def t100(
        cls,
        sso_version: int,
        app_id: int,
        sub_app_id: int,
        app_client_version: int,
        sigmap: int,
        _db_buf_ver: int = 1,
    ) -> "Packet[()]":
        return cls._pack_tlv(
            0x100,
            struct.pack(
                ">HIIIII",
                _db_buf_ver,
                sso_version,
                app_id,
                sub_app_id,
                app_client_version,
                sigmap,
            ),
        )

    @classmethod
    def t104(cls, data: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x104, data)

    @classmethod
    def t106(
        cls,
        sso_version: int,
        app_id: int,
        sub_app_id: int,
        app_client_version: int,
        uin: int,
        salt: int,
        password_md5: bytes,
        guid: bytes,
        tgtgt_key: bytes,
        ip: bytes = bytes(4),
        save_password: bool = True,
        login_type: int = 1,  # password login
    ) -> "Packet[()]":
        key = md5(
            Packet.build(password_md5, bytes(4), struct.pack(">I", salt or uin))
        ).digest()

        body = Packet.build(
            struct.pack(
                ">HIIIIQ",
                4,  # tgtgt version
                cls._random_int32(),
                sso_version,
                app_id,
                app_client_version,
                uin or salt,
            ),
            struct.pack(">I", int(time.time())),
            ip,
            struct.pack(">?", save_password),
            struct.pack(">16s", password_md5),
            tgtgt_key,
            struct.pack(">I?", 0, bool(guid)),
            guid
            or struct.pack(
                ">IIII",
                cls._random_int32(),
                cls._random_int32(),
                cls._random_int32(),
                cls._random_int32(),
            ),
            struct.pack(">II", sub_app_id, login_type),
            cls._pack_lv(str(uin).encode()),
            struct.pack(">H", 0),  # not found in source
        )

        data = qqtea_encrypt(bytes(body), key)
        return cls._pack_tlv(0x106, data)

    @classmethod
    def t107(
        cls,
        pic_type: int = 0,
        cap_type: int = 0,
        pic_size: int = 0,
        ret_type: int = 1,
    ) -> "Packet[()]":
        return cls._pack_tlv(
            0x107, struct.pack(">HBHB", pic_type, cap_type, pic_size, ret_type)
        )

    @classmethod
    def t108(cls, ksid: str) -> "Packet[()]":
        return cls._pack_tlv(0x108, ksid.encode())

    @classmethod
    def t109(cls, android_id: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x109, md5(android_id).digest())

    @classmethod
    def t10a(cls, arr: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x10A, arr)

    @classmethod
    def t112(cls, non_number_uin: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x112, non_number_uin)

    @classmethod
    def t116(
        cls,
        bitmap: int,
        sub_sigmap: int,
        sub_app_id_list: List[int] = [1600000226],
        _ver: int = 0,
    ) -> "Packet[()]":
        return cls._pack_tlv(
            0x116,
            struct.pack(
                ">BIIB", _ver, bitmap, sub_sigmap, len(sub_app_id_list)
            ),
            *[struct.pack(">I", id) for id in sub_app_id_list],
        )

    @classmethod
    def t124(
        cls,
        os_type: bytes,
        os_version: bytes,
        network_type: int,
        sim_info: bytes,
        apn: bytes,
        address: bytes = bytes(),
    ) -> "Packet[()]":
        return cls._pack_tlv(
            0x124,
            cls._pack_lv_limited(os_type, 16),
            cls._pack_lv_limited(os_version, 16),
            struct.pack(">H", network_type),
            cls._pack_lv_limited(sim_info, 16),
            cls._pack_lv_limited(address, 32),
            cls._pack_lv_limited(apn, 16),
        )

    @classmethod
    def t128(
        cls,
        is_guid_from_file_null: bool,
        is_guid_available: bool,
        is_guid_changed: bool,
        guid_flag: int,
        build_model: bytes,
        guid: bytes,
        build_brand: bytes,
    ) -> "Packet[()]":
        """
        :GUID_SRC:
            * 0: 初始值
            * 1: 以前保存的文件
            * 17: 以前没保存但现在生成成功
            * 20: 以前没保存且现在生成失败

        :GUID_CHANGE_FLAG:
            * mac != current mac: ``GUID_CHANGE_FLAG |= 0x1``
            * android_id != current android_id: ``GUID_CHANGE_FLAG |= 0x2``
            * guid != current guid: ``GUID_CHANGE_FLAG |= 0x4``

        Example:

            >>> GUID_FLAG = 0
            >>> GUID_FLAG |= GUID_SRC << 24 & 0xFF000000
            >>> GUID_FLAG |= GUID_CHANGE_FLAG << 8 & 0xFF00

        """
        return cls._pack_tlv(
            0x128,
            struct.pack(
                ">H???I",
                0,
                is_guid_from_file_null,
                is_guid_available,
                is_guid_changed,
                guid_flag,
            ),
            cls._pack_lv_limited(build_model, 32),
            cls._pack_lv_limited(guid, 16),
            cls._pack_lv_limited(build_brand, 16),
        )

    @classmethod
    def t141(
        cls, sim_info: bytes, network_type: int, apn: bytes, _version: int = 1
    ) -> "Packet[()]":
        return cls._pack_tlv(
            0x141,
            struct.pack(">H", _version),
            cls._pack_lv(sim_info),
            struct.pack(">H", network_type),
            cls._pack_lv(apn),
        )

    @classmethod
    def t142(cls, apk_id: str, _version: int = 0) -> "Packet[()]":
        return cls._pack_tlv(
            0x142,
            struct.pack(">H", _version),
            cls._pack_lv_limited(apk_id.encode(), 32),
        )

    @classmethod
    def t143(cls, arr: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x143, arr)

    @classmethod
    def t144(
        cls,
        imei: bytes,
        bootloader: str,
        proc_version: str,
        codename: str,
        incremental: str,
        fingerprint: str,
        boot_id: str,
        android_id: str,
        baseband: str,
        inner_version: str,
        os_type: bytes,
        os_version: bytes,
        network_type: int,
        sim_info: bytes,
        apn: bytes,
        is_guid_from_file_null: bool,
        is_guid_available: bool,
        is_guid_changed: bool,
        guid_flag: int,
        build_model: bytes,
        guid: bytes,
        build_brand: bytes,
        tgtgt_key: bytes,
    ) -> "Packet[()]":
        return cls._pack_tlv(
            0x144,
            qqtea_encrypt(
                bytes(
                    Packet.build(
                        struct.pack(">H", 5),  # tlv count
                        cls.t109(imei),
                        cls.t52d(
                            bootloader,
                            proc_version,
                            codename,
                            incremental,
                            fingerprint,
                            boot_id,
                            android_id,
                            baseband,
                            inner_version,
                        ),
                        cls.t124(
                            os_type, os_version, network_type, sim_info, apn
                        ),
                        cls.t128(
                            is_guid_from_file_null,
                            is_guid_available,
                            is_guid_changed,
                            guid_flag,
                            build_model,
                            guid,
                            build_brand,
                        ),
                        cls.t16e(build_model),
                    )
                ),
                tgtgt_key,
            ),
        )

    @classmethod
    def t145(cls, guid: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x145, guid)

    @classmethod
    def t147(
        cls, app_id: int, apk_version_name: bytes, apk_signature_md5: bytes
    ) -> "Packet[()]":
        return cls._pack_tlv(
            0x147,
            struct.pack(">I", app_id),
            cls._pack_lv_limited(apk_version_name, 32),
            cls._pack_lv_limited(apk_signature_md5, 32),
        )

    @classmethod
    def t154(cls, seq: int) -> "Packet[()]":
        return cls._pack_tlv(0x154, struct.pack(">I", seq))

    @classmethod
    def t166(cls, image_type: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x166, struct.pack(">c", image_type))

    @classmethod
    def t16a(cls, no_pic_sig: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x16A, no_pic_sig)

    @classmethod
    def t16e(cls, build_model: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x16E, build_model)

    @classmethod
    def t172(cls, rollback_sig: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x172, rollback_sig)

    @classmethod
    def t174(cls, data: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x174, data)

    @classmethod
    def t177(cls, build_time: int, sdk_version: str) -> "Packet[()]":
        return cls._pack_tlv(
            0x177,
            struct.pack(">BI", 1, build_time),
            cls._pack_lv(sdk_version.encode()),
        )

    @classmethod
    def t17a(cls, sms_app_id: int) -> "Packet[()]":
        return cls._pack_tlv(0x17A, struct.pack(">I", sms_app_id))

    @classmethod
    def t17c(cls, code: str) -> "Packet[()]":
        return cls._pack_tlv(0x17C, cls._pack_lv(code.encode()))

    @classmethod
    def t185(cls) -> "Packet[()]":
        return cls._pack_tlv(0x185, bytes([1, 1]))

    @classmethod
    def t187(cls, mac_address: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x187, md5(mac_address).digest())

    @classmethod
    def t188(cls, android_id: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x188, md5(android_id).digest())

    @classmethod
    def t191(cls, can_web_verify: int) -> "Packet[()]":
        return cls._pack_tlv(0x191, struct.pack(">B", can_web_verify))

    @classmethod
    def t193(cls, ticket: str) -> "Packet[()]":
        return cls._pack_tlv(0x193, ticket.encode())

    @classmethod
    def t194(cls, imsi_md5: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x194, imsi_md5)

    @classmethod
    def t197(cls, data: bytes = bytes(1)) -> "Packet[()]":
        return cls._pack_tlv(0x197, data)

    @classmethod
    def t198(cls) -> "Packet[()]":
        return cls._pack_tlv(0x198, bytes(1))

    @classmethod
    def t19e(cls, value: int = 1) -> "Packet[()]":
        return cls._pack_tlv(0x19E, struct.pack(">HB", 1, value))

    @classmethod
    def t201(
        cls, channel_id: bytes, client_type: bytes, n: bytes, l: bytes = bytes()
    ) -> "Packet[()]":
        return cls._pack_tlv(
            0x201,
            cls._pack_lv(l),
            cls._pack_lv(channel_id),
            cls._pack_lv(client_type),
            cls._pack_lv(n),
        )

    @classmethod
    def t202(cls, wifi_bssid: bytes, wifi_ssid: bytes) -> "Packet[()]":
        return cls._pack_tlv(
            0x202,
            cls._pack_lv_limited(wifi_bssid, 16),
            cls._pack_lv_limited(wifi_ssid, 32),
        )

    @classmethod
    def t318(cls, tgt_qr: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x318, tgt_qr)

    @classmethod
    def t400(
        cls,
        g: bytes,
        uin: int,
        guid: bytes,
        dpwd: bytes,
        app_id: int,
        sub_app_id: int,
        rand_seed: bytes,
        _version: int = 1,
    ) -> "Packet[()]":
        data = Packet.build(
            struct.pack(">HQ", _version, uin),
            guid,
            dpwd,
            struct.pack(">III", app_id, sub_app_id, int(time.time())),
            rand_seed,
        )
        return cls._pack_tlv(0x400, qqtea_encrypt(bytes(data), g))

    @classmethod
    def t401(cls, data: bytes) -> "Packet[()]":
        return cls._pack_tlv(0x401, data)

    @classmethod
    def t511(cls, domains: List[str]) -> "Packet[()]":
        _domains = [domain for domain in domains if domain]

        data: List[Union[bytes, "Packet[()]"]] = []
        for domain in _domains:
            index1 = domain.find("(")
            index2 = domain.find(")")
            if index1 != 0 or index2 <= 0:
                data.append(bytes([1]))
                data.append(cls._pack_lv(domain.encode()))
            else:
                try:
                    i = int(domain[index1 + 1 : index2])
                    data.append(
                        struct.pack(
                            ">B",
                            (((i & 0x8000000) > 0) << 1) | ((0x100000 & i) > 0),
                        )
                    )
                    data.append(cls._pack_lv(domain[index2 + 1 :].encode()))
                except Exception:
                    pass
        return cls._pack_tlv(0x511, struct.pack(">H", len(_domains)), *data)

    @classmethod
    def t516(cls, source_type: int = 0) -> "Packet[()]":
        return cls._pack_tlv(0x516, struct.pack(">I", source_type))

    @classmethod
    def t521(cls, product_type: int = 0) -> "Packet[()]":
        return cls._pack_tlv(0x521, struct.pack(">IH", product_type, 0))

    @classmethod
    def t525(cls, t536: "Packet[()]") -> "Packet[()]":
        return cls._pack_tlv(0x525, struct.pack(">H", 1), t536)

    @classmethod
    def t52c(cls) -> "Packet[()]":
        return cls._pack_tlv(0x52C, struct.pack(">BQ", 1, -1))

    @classmethod
    def t52d(
        cls,
        bootloader: str,
        proc_version: str,
        codename: str,
        incremental: str,
        fingerprint: str,
        boot_id: str,
        android_id: str,
        baseband: str,
        inner_version: str,
    ) -> "Packet[()]":
        """
        Note:
            Source: oicq.wlogin_sdk.tools.util#get_android_dev_info
        """
        device_info = DeviceReport(
            bootloader=bootloader,
            proc_version=proc_version,
            codename=codename,
            incremental=incremental,
            fingerprint=fingerprint,
            boot_id=boot_id,
            android_id=android_id,
            base_band=baseband,
            inner_version=inner_version,
        )
        return cls._pack_tlv(0x52D, device_info.SerializeToString())

    @classmethod
    def t536(cls, login_extra_data: List[bytes]) -> "Packet[()]":
        return cls._pack_tlv(
            0x536,
            struct.pack(">BB", 1, len(login_extra_data)),
            *login_extra_data,
        )

    @classmethod
    def t544(cls) -> "Packet[()]":
        return cls._pack_tlv(0x544, bytes([0, 0, 0, 11]))


class TlvDecoder:
    @classmethod
    def decode(
        cls,
        data: Union[bytes, "Packet[()]"],
        offset: int = 0,
        tag_size: int = 2,
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
            offset += length
            futher_decode = getattr(cls, f"t{tag:x}", None)
            if futher_decode:
                value = futher_decode(value)
            result[tag] = value

        return result

    @classmethod
    def t113(cls, data: bytes) -> Dict[str, Any]:
        """Decode tlv 113 data.

        Data:
            * uin (int): user QQ number.

        Note:
            Source: oicq.wlogin_sdk.tlv_type.tlv_t113
        """
        return {"uin": struct.unpack_from(">I", data)[0]}

    @classmethod
    def t119(cls, data: bytes) -> Dict[int, Any]:
        """Tea decrypt tlv 119 data.

        Tlv list:
            * tlv 149: error message (optional).
            * tlv 543:
            * tlv 130: further decode.
            * tlv 113: further decode.
            * tlv 528:
            * tlv 530:
            * tlv 10d: tgt key.
            * tlv 10e: st key.
            * tlv 10a: tgt.
            * tlv 114: st.
            * tlv 11a: further decode.
            * tlv 118: main display name.
            * tlv 103: stwx web sig.
            * tlv 108: ksid.
            * tlv 102:
            * tlv 10b:
            * tlv 11c: ls key.
            * tlv 120: skey.
            * tlv 121: sig64.
            * tlv 125: further decode.
            * tlv 186: further decode.
            * tlv 537: login extra data.
            * tlv 169:
            * tlv 167:
            * tlv 10c:
            * tlv 106: encrypted a1.
            * tlv 16a: no pic sig.
            * tlv 531: further decode.
            * tlv 136: vkey.
            * tlv 132: access token.
            * tlv 143: d2.
            * tlv 305: d2 key.
            * tlv 164: sid.
            * tlv 171: aq sig.
            * tlv 512: ps key.
            * tlv 16d: super key.
            * tlv 199: further decode.
            * tlv 200: further decode.
            * tlv 203: pfkey.
            * tlv 317: da2.
            * tlv 133: wt session ticket.
            * tlv 134: wt session ticket key.
            * tlv 322: device token.
            * tlv 11f: futher decode. change time and tk_pri.
            * tlv 138: further decode. a2, lskey, skey, vkey, a8, stweb, d2, sid change time.
            * tlv 11d: further decode. st and stkey.

        Note:
            Source: oicq.wlogin_sdk.request.oicq_request.d
        """
        data = qqtea_decrypt(data, DEVICE.tgtgt)
        result = cls.decode(data, offset=2)
        return result

    @classmethod
    def t11a(cls, data: bytes) -> Dict[str, Any]:
        """Decode tlv 11a data.

        Data:
            * face (bytes(2))
            * age (int)
            * gender (int)
            * nick (str)

        Note:
            Source: oicq.wlogin_sdk.tlv_type.tlv_t11a
        """
        data_ = Packet(data)
        return {
            "face": data_.read_bytes(2),
            "age": data_.read_uint8(offset=2),
            "gender": data_.read_uint8(offset=3),
            "nick": data_.read_bytes(
                data_.read_uint8(offset=4), offset=5
            ).decode(),
        }

    @classmethod
    def t125(cls, data: bytes) -> Dict[str, Any]:
        """Decode tlv 125 data.

        Data:
            * open_id (bytes)
            * open_key (bytes)

        Note:
            Source: oicq.wlogin_sdk.tlv_type.tlv_t125
        """
        data_ = Packet(data)
        offset = 0
        id_length = data_.read_uint16(offset)
        offset += 2 + id_length
        key_length = data_.read_uint16(offset)
        return {
            "open_id": data_.read_bytes(id_length, 2),
            "open_key": data_.read_bytes(key_length, offset + 2),
        }

    @classmethod
    def t130(cls, data: bytes) -> Dict[str, Any]:
        """Decode tlv 130 data.

        Data:
            * time_diff (int): time difference between server and local.
            * ip_address (bytes(4)): may be server ip

        Note:
            Source: oicq.wlogin_sdk.tlv_type.tlv_t130
        """
        data_ = Packet(data)
        return {
            "time_diff": data_.read_int32(offset=2) - int(time.time()),
            "ip_address": data_.read_bytes(4, offset=6),
        }

    # @classmethod
    # def t138(cls, data: bytes) -> Dict[str, Any]:
    #     return {}

    @classmethod
    def t161(cls, data: bytes) -> Dict[int, bytes]:
        """Decode tlv 161 data.

        Tlv list:
            * tlv 172: rollback sig.
            * tlv 173: further decode.
            * tlv 17f: further decode.

        Note:
            Source: oicq.wlogin_sdk.request.oicq_request.a
        """
        result = cls.decode(data, offset=2)
        return result

    @classmethod
    def t186(cls, data: bytes) -> Dict[str, Any]:
        """Decode tlv 186 data.

        Data:
            * pwd_flag (bool)

        Note:
            Source: oicq.wlogin_sdk.tlv_type.tlv_t186
        """
        return {"pwd_flag": data[1] == bytes([1])}

    @classmethod
    def t199(cls, data: bytes) -> Dict[str, Any]:
        """Decode tlv 199 data.

        Data:
            * open_id (bytes)
            * pay_token (bytes)

        Note:
            Source: oicq.wlogin_sdk.tlv_type.tlv_t199
        """
        data_ = Packet(data)
        offset = 0
        id_length = data_.read_uint16(offset)
        offset += 2 + id_length
        token_length = data_.read_uint16(offset)
        return {
            "open_id": data_.read_bytes(id_length, 2),
            "pay_token": data_.read_bytes(token_length, offset + 2),
        }

    @classmethod
    def t200(cls, data: bytes) -> Dict[str, Any]:
        """Decode tlv 200 data.

        Data:
            * pf (bytes)
            * pf_key (bytes)

        Note:
            Source: oicq.wlogin_sdk.tlv_type.tlv_t200
        """
        data_ = Packet(data)
        offset = 0
        pf_length = data_.read_uint16(offset)
        offset += 2 + pf_length
        key_length = data_.read_uint16(offset)
        return {
            "pf": data_.read_bytes(pf_length, 2),
            "pf_key": data_.read_bytes(key_length, offset + 2),
        }

    @classmethod
    def t512(cls, data: bytes) -> Dict[str, Any]:
        data_ = Packet(data)
        offset = 0
        length = data_.read_uint16()
        offset += 2

        ps_key_map: Dict[str, bytes] = {}
        pt4_token_map: Dict[str, bytes] = {}
        for _ in range(length):
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
            pt4_token_map[domain] = ps4_token

        return {"ps_key_map": ps_key_map, "pt4_token_map": pt4_token_map}

    @classmethod
    def t531(cls, data: bytes) -> Dict[str, Any]:
        """Tea decrypt tlv 119 data.

        Tlv list:
            * tlv 106: a1 part.
            * tlv 10c: a1 part.
            * tlv 16a: no pic sig.
            * tlv 113:

        Note:
            Source: oicq.wlogin_sdk.request.oicq_request.d
        """
        result = cls.decode(data)
        return {
            "a1": (result.get(0x106, b"") + result.get(0x10C, b"")) or None,
            "no_pic_sig": result.get(0x16A),
        }
