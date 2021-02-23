"""OICQ Packet Builder

This module is used to build and handle OICQ packets.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import time
import struct
from dataclasses import dataclass
from typing import Any, Dict, Union, Optional

from .tlv import TlvDecoder
from cai.client.event import Event
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


@dataclass
class OICQResponse(Event):

    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "OICQResponse":
        if ret_code != 0 or not data:
            return OICQResponse(uin, seq, ret_code, command_name)

        data_ = Packet(data)

        offset = 0
        sub_command = data_.read_uint16(offset)
        offset += 2
        status = data_.read_uint8(offset)
        offset += 1 + 2
        _tlv_map = TlvDecoder.decode(data_, offset)

        if status == 0:
            return LoginSuccess(
                uin, seq, ret_code, command_name, sub_command, status, _tlv_map
            )
        elif status == 2:
            return NeedCaptcha(
                uin, seq, ret_code, command_name, sub_command, status, _tlv_map
            )
        else:
            return UnknownLoginStatus(
                uin, seq, ret_code, command_name, sub_command, status, _tlv_map
            )


@dataclass
class UnknownLoginStatus(OICQResponse):
    sub_command: int
    status: int
    _tlv_map: Dict[int, Any]

    t402: Optional[bytes]

    def __init__(
        self, uin: int, seq: int, ret_code: int, command_name: str,
        sub_command: int, status: int, _tlv_map: Dict[int, Any]
    ):
        super().__init__(uin, seq, ret_code, command_name)
        self.sub_command = sub_command
        self.status = status
        self._tlv_map = _tlv_map

        self.t402 = _tlv_map.get(0x402)


@dataclass
class LoginSuccess(UnknownLoginStatus):
    nick: Optional[str]
    age: Optional[int]
    gender: Optional[int]
    ksid: Optional[bytes]
    time_diff: Optional[int]
    pwd_flag: Optional[bool]
    rand_seed: Optional[bytes]
    rollback_sig: Optional[bytes]

    tgt: bytes
    tgt_key: bytes
    srm_token: bytes
    t133: bytes
    encrypted_a1: bytes
    user_st_key: bytes
    user_st_web_sig: bytes
    s_key: bytes
    s_key_expire_time: int
    d2: bytes
    d2key: bytes
    wt_session_ticket_key: bytes
    device_token: bytes
    ps_key_map: Dict[str, bytes]
    pt4_token_map: Dict[str, bytes]

    t149: Optional[bytes]
    t150: Optional[bytes]
    t528: Optional[bytes]
    t530: Optional[bytes]

    def __init__(
        self, uin: int, seq: int, ret_code: int, command_name: str,
        sub_command: int, status: int, _tlv_map: Dict[int, Any]
    ):
        super().__init__(
            uin, seq, ret_code, command_name, sub_command, status, _tlv_map
        )
        self.t150 = _tlv_map.get(0x150)
        self.rollback_sig = _tlv_map.get(0x161, {}).get(0x172)
        self.rand_seed = _tlv_map.get(0x403)

        t119 = _tlv_map.get(0x119, {})
        self.time_diff = t119.get(0x130, {}).get("time_diff")
        self.t149 = t119.get(0x130, {}).get("t149")
        self.t528 = t119.get(0x528)
        self.t530 = t119.get(0x530)
        self.ksid = t119.get(0x108)
        self.pwd_flag = t119.get(0x186, {}).get("pwd_flag")
        self.nick = t119.get(0x11a, {}).get("nick")
        self.age = t119.get(0x11a, {}).get("age")
        self.gender = t119.get(0x11a, {}).get("gender")
        self.ps_key_map = t119.get(0x512, {}).get("ps_key_map", {})
        self.pt4_token_map = t119.get(0x512, {}).get("pt4_token_map", {})

        self.srm_token = _tlv_map[0x16a]
        self.t133 = _tlv_map[0x133]
        self.encrypted_a1 = _tlv_map[0x106]
        self.tgt = _tlv_map[0x10a]
        self.tgt_key = _tlv_map[0x10d]
        self.user_st_key = _tlv_map[0x10e]
        self.user_st_web_sig = _tlv_map[0x103]
        self.s_key = _tlv_map[0x120]
        self.s_key_expire_time = int(time.time()) + 21600
        self.d2 = _tlv_map[0x143]
        self.d2key = _tlv_map[0x305]
        self.wt_session_ticket_key = _tlv_map[0x134]
        self.device_token = _tlv_map[0x322]


@dataclass
class NeedCaptcha(UnknownLoginStatus):
    t104: bytes
    verify_url: str
    captcha_image: bytes
    captcha_sign: bytes

    def __init__(
        self, uin: int, seq: int, ret_code: int, command_name: str,
        sub_command: int, status: int, _tlv_map: Dict[int, Any]
    ):
        super().__init__(
            uin, seq, ret_code, command_name, sub_command, status, _tlv_map
        )
        self.t104 = _tlv_map[0x104]
        self.verify_url = _tlv_map.get(0x192, b"").decode()
        if 0x165 in _tlv_map:
            data = Packet(_tlv_map[0x165])
            sign_length = data.read_uint16()
            self.captcha_sign = data.read_bytes(sign_length, 4)
            self.captcha_image = data[4 + sign_length:]
