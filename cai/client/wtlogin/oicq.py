"""OICQ Packet Builder

This module is used to build and handle OICQ packets.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
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
        cls,
        uin: int,
        command_id: int,
        encoded: Union[bytes, Packet],
        encoder_id: int,
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
                0,
            ),
            encoded,
            bytes([3]),
        )


@dataclass
class OICQResponse(Event):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "OICQResponse":
        """Decode login response and wrap main info of the response.

        Note:
            Source: oicq.wlogin_sdk.request.WtloginHelper.GetStWithPasswd

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.

        Returns:
            LoginSuccess: Login success.
            NeedCaptcha: Captcha image needed.
            AccountFrozen: Account is frozen.
            DeviceLocked: Device lock detected.
            TooManySMSRequest: Too many SMS messages were sent.
            DeviceLockLogin: More login packet needed.
            UnknownLoginStatus: Unknown login status.
            OICQResponse: Invalid login response.
        """
        if ret_code != 0 or not data:
            return OICQResponse(uin, seq, ret_code, command_name)

        data_ = Packet(data)

        sub_command, status, _tlv_bytes = (
            data_.uint16().uint8().offset(2).remain().execute()
        )

        _tlv_map = TlvDecoder.decode(_tlv_bytes)

        if status == 0:
            return LoginSuccess(
                uin, seq, ret_code, command_name, sub_command, status, _tlv_map
            )
        elif status == 2:
            return NeedCaptcha(
                uin, seq, ret_code, command_name, sub_command, status, _tlv_map
            )
        elif status == 40:
            return AccountFrozen(
                uin, seq, ret_code, command_name, sub_command, status, _tlv_map
            )
        elif status == 160 or status == 239:
            return DeviceLocked(
                uin, seq, ret_code, command_name, sub_command, status, _tlv_map
            )
        elif status == 162:
            return TooManySMSRequest(
                uin, seq, ret_code, command_name, sub_command, status, _tlv_map
            )
        elif status == 204:
            return DeviceLockLogin(
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
        self,
        uin: int,
        seq: int,
        ret_code: int,
        command_name: str,
        sub_command: int,
        status: int,
        _tlv_map: Dict[int, Any],
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
    ip_address: Optional[bytes]
    pwd_flag: Optional[bool]
    rand_seed: Optional[bytes]
    rollback_sig: Optional[bytes]

    tgt: bytes
    tgt_key: bytes
    no_pic_sig: bytes
    encrypted_a1: bytes
    user_st: bytes
    user_st_key: bytes
    user_st_web_sig: bytes
    s_key: bytes
    d2: bytes
    d2key: bytes
    wt_session_ticket: bytes
    wt_session_ticket_key: bytes
    device_token: Optional[bytes]
    ps_key_map: Dict[str, bytes]
    pt4_token_map: Dict[str, bytes]

    t150: Optional[bytes]
    t528: Optional[bytes]
    t530: Optional[bytes]

    def __init__(
        self,
        uin: int,
        seq: int,
        ret_code: int,
        command_name: str,
        sub_command: int,
        status: int,
        _tlv_map: Dict[int, Any],
    ):
        super().__init__(
            uin, seq, ret_code, command_name, sub_command, status, _tlv_map
        )
        self.t150 = _tlv_map.get(0x150)
        self.rollback_sig = _tlv_map.get(0x161, {}).get(0x172)
        self.rand_seed = _tlv_map.get(0x403)

        t119 = _tlv_map.get(0x119, {})
        self.time_diff = t119.get(0x130, {}).get("time_diff")
        self.ip_address = t119.get(0x130, {}).get("ip_address")
        self.t528 = t119.get(0x528)
        self.t530 = t119.get(0x530)
        self.tgt_key = t119[0x10D]
        self.user_st_key = t119[0x10E]
        self.tgt = t119[0x10A]
        self.user_st = t119[0x114]
        self.nick = t119.get(0x11A, {}).get("nick")
        self.age = t119.get(0x11A, {}).get("age")
        self.gender = t119.get(0x11A, {}).get("gender")
        self.user_st_web_sig = t119[0x103]
        self.ksid = t119.get(0x108)
        self.s_key = t119[0x120]
        self.pwd_flag = t119.get(0x186, {}).get("pwd_flag")
        self.encrypted_a1 = t119[0x106]
        self.no_pic_sig = t119[0x16A]

        self.d2 = t119[0x143]
        self.d2key = t119[0x305]
        self.ps_key_map = t119.get(0x512, {}).get("ps_key_map", {})
        self.pt4_token_map = t119.get(0x512, {}).get("pt4_token_map", {})
        self.wt_session_ticket = t119[0x133]
        self.wt_session_ticket_key = t119[0x134]
        self.device_token = t119.get(0x322, None)


@dataclass
class NeedCaptcha(UnknownLoginStatus):
    t104: bytes
    verify_url: str
    captcha_sign: bytes
    captcha_image: bytes

    def __init__(
        self,
        uin: int,
        seq: int,
        ret_code: int,
        command_name: str,
        sub_command: int,
        status: int,
        _tlv_map: Dict[int, Any],
    ):
        super().__init__(
            uin, seq, ret_code, command_name, sub_command, status, _tlv_map
        )
        self.t104 = _tlv_map[0x104]
        self.captcha_image = bytes()
        self.captcha_sign = bytes()
        self.verify_url = _tlv_map.get(0x192, b"").decode()
        if 0x165 in _tlv_map:
            data = Packet(_tlv_map[0x165])
            sign, image = data.bytes_with_length(2, 4).remain().execute()
            self.captcha_sign = sign[2:]
            self.captcha_image = bytes(image)


@dataclass
class AccountFrozen(UnknownLoginStatus):
    def __init__(
        self,
        uin: int,
        seq: int,
        ret_code: int,
        command_name: str,
        sub_command: int,
        status: int,
        _tlv_map: Dict[int, Any],
    ):
        super().__init__(
            uin, seq, ret_code, command_name, sub_command, status, _tlv_map
        )


@dataclass
class DeviceLocked(UnknownLoginStatus):
    sms_phone: Optional[str]
    verify_url: Optional[str]
    message: Optional[str]
    rand_seed: Optional[bytes]
    t104: Optional[bytes]
    t174: Optional[bytes]

    def __init__(
        self,
        uin: int,
        seq: int,
        ret_code: int,
        command_name: str,
        sub_command: int,
        status: int,
        _tlv_map: Dict[int, Any],
    ):
        super().__init__(
            uin, seq, ret_code, command_name, sub_command, status, _tlv_map
        )
        self.sms_phone = None
        self.verify_url = _tlv_map.get(0x204, b"").decode() or None
        self.message = _tlv_map.get(0x17E, b"").decode() or None
        self.rand_seed = _tlv_map.get(0x403)
        self.t104 = _tlv_map.get(0x104)
        self.t174 = _tlv_map.get(0x174)
        if self.t174:
            t178 = Packet(_tlv_map[0x178])
            self.sms_phone = t178.string(4).execute()[0]


@dataclass
class TooManySMSRequest(UnknownLoginStatus):
    def __init__(
        self,
        uin: int,
        seq: int,
        ret_code: int,
        command_name: str,
        sub_command: int,
        status: int,
        _tlv_map: Dict[int, Any],
    ):
        super().__init__(
            uin, seq, ret_code, command_name, sub_command, status, _tlv_map
        )


@dataclass
class DeviceLockLogin(UnknownLoginStatus):
    rand_seed: Optional[bytes]
    t104: Optional[bytes]

    def __init__(
        self,
        uin: int,
        seq: int,
        ret_code: int,
        command_name: str,
        sub_command: int,
        status: int,
        _tlv_map: Dict[int, Any],
    ):
        super().__init__(
            uin, seq, ret_code, command_name, sub_command, status, _tlv_map
        )
        self.rand_seed = _tlv_map.get(0x403)
        self.t104 = _tlv_map.get(0x104)
