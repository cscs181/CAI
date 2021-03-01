"""Login Related SDK

This module is used to build and handle login related packet.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import time
import struct
import ipaddress

from .tlv import TlvEncoder
from cai.utils.ecdh import ECDH
from cai.utils.binary import Packet
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol
from .oicq import (
    OICQRequest, OICQResponse, LoginSuccess, NeedCaptcha, AccountFrozen,
    DeviceLocked, TooManySMSRequest, DeviceLockLogin, UnknownLoginStatus
)
from cai.client.packet import CSsoBodyPacket, CSsoDataPacket, IncomingPacket

DEVICE = get_device()
APK_INFO = get_protocol()


# submit captcha
def encode_login_request2_captcha(
    seq: int, key: bytes, session_id: bytes, ksid: bytes, uin: int,
    captcha: str, sign: bytes, t104: bytes
):
    """Build submit captcha request packet.

    Called in `oicq.wlogin_sdk.request.WtloginHelper.CheckPictureAndGetSt`.

    command id: `0x810 = 2064`

    sub command id: `2`

    command name: `wtlogin.login`

    Note:
        Source: oicq.wlogin_sdk.request.n

    Args:
        seq (int): Packet sequence.
        key (bytes): 16 bits key used to decode the response.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        captcha (str): Captcha image result.
        sign (bytes): Signature of the captcha.
        t104 (bytes): TLV 104 data.


    Returns:
        Packet: Login packet.
    """
    COMMAND_ID = 2064
    SUB_COMMAND_ID = 2
    COMMAND_NAME = "wtlogin.login"

    SUB_APP_ID = APK_INFO.sub_app_id
    BITMAP = APK_INFO.bitmap
    SUB_SIGMAP = APK_INFO.sub_sigmap

    LOCAL_ID = 2052  # oicq.wlogin_sdk.request.t.v

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 4),  # packet num
        TlvEncoder.t2(captcha.encode(), sign),
        TlvEncoder.t8(LOCAL_ID),
        TlvEncoder.t104(t104),
        TlvEncoder.t116(BITMAP, SUB_SIGMAP)
    )
    oicq_packet = OICQRequest.build_encoded(
        uin, COMMAND_ID, ECDH.encrypt(data, key), ECDH.id
    )
    sso_packet = CSsoBodyPacket.build(
        seq, SUB_APP_ID, COMMAND_NAME, DEVICE.imei, session_id, ksid,
        oicq_packet
    )
    # encrypted by 16-byte zero. Reference: `CSSOData::serialize`
    packet = CSsoDataPacket.build(uin, 2, sso_packet, key=bytes(16))
    return packet


# submit ticket
def encode_login_request2_slider(
    seq: int, key: bytes, session_id: bytes, ksid: bytes, uin: int, ticket: str,
    t104: bytes
):
    """Build slider ticket request packet.

    Called in `oicq.wlogin_sdk.request.WtloginHelper.CheckPictureAndGetSt`.

    command id: `0x810 = 2064`

    sub command id: `2`

    command name: `wtlogin.login`

    Note:
        Source: oicq.wlogin_sdk.request.n

    Args:
        seq (int): Packet sequence.
        key (bytes): 16 bits key used to decode the response.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        ticket (str): Captcha image result.
        t104 (bytes): TLV 104 data.


    Returns:
        Packet: Login packet.
    """
    COMMAND_ID = 2064
    SUB_COMMAND_ID = 2
    COMMAND_NAME = "wtlogin.login"

    SUB_APP_ID = APK_INFO.sub_app_id
    BITMAP = APK_INFO.bitmap
    SUB_SIGMAP = APK_INFO.sub_sigmap

    LOCAL_ID = 2052  # oicq.wlogin_sdk.request.t.v

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 4),  # packet num
        TlvEncoder.t193(ticket),
        TlvEncoder.t8(LOCAL_ID),
        TlvEncoder.t104(t104),
        TlvEncoder.t116(BITMAP, SUB_SIGMAP)
    )
    oicq_packet = OICQRequest.build_encoded(
        uin, COMMAND_ID, ECDH.encrypt(data, key), ECDH.id
    )
    sso_packet = CSsoBodyPacket.build(
        seq, SUB_APP_ID, COMMAND_NAME, DEVICE.imei, session_id, ksid,
        oicq_packet
    )
    # encrypted by 16-byte zero. Reference: `CSSOData::serialize`
    packet = CSsoDataPacket.build(uin, 2, sso_packet, key=bytes(16))
    return packet


# password md5 login
def encode_login_request9(
    seq: int, key: bytes, session_id: bytes, ksid: bytes, uin: int,
    password_md5: bytes
):
    """Build main login request packet.

    Called in `oicq.wlogin_sdk.request.WtloginHelper.GetStWithPasswd`.

    command id: `0x810 = 2064`

    sub command id: `9`

    command name: `wtlogin.login`

    Note:
        Source: oicq.wlogin_sdk.request.k

    Args:
        seq (int): Packet sequence.
        key (bytes): 16 bits key used to decode the response.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        password_md5 (bytes): User QQ password md5 hash.

    Returns:
        Packet: Login packet.
    """
    COMMAND_ID = 2064
    SUB_COMMAND_ID = 9
    COMMAND_NAME = "wtlogin.login"

    APK_ID = APK_INFO.apk_id
    APK_VERSION = APK_INFO.version
    APK_SIGN = APK_INFO.apk_sign
    APK_BUILD_TIME = APK_INFO.build_time
    APP_ID = APK_INFO.app_id
    SUB_APP_ID = APK_INFO.sub_app_id
    APP_CLIENT_VERSION = 0
    SDK_VERSION = APK_INFO.sdk_version
    SSO_VERSION = APK_INFO.sso_version
    BITMAP = APK_INFO.bitmap
    MAIN_SIGMAP = APK_INFO.main_sigmap
    SUB_SIGMAP = APK_INFO.sub_sigmap

    GUID_SRC = 1
    GUID_CHANGE = 0
    GUID_FLAG = 0
    GUID_FLAG |= GUID_SRC << 24 & 0xFF000000
    GUID_FLAG |= GUID_CHANGE << 8 & 0xFF00
    CAN_WEB_VERIFY = 130  # oicq.wlogin_sdk.request.k.K
    LOCAL_ID = 2052  # oicq.wlogin_sdk.request.t.v
    IP_BYTES: bytes = ipaddress.ip_address(DEVICE.ip_address).packed
    NETWORK_TYPE = (DEVICE.apn == "wifi") + 1

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 23),  # packet num
        TlvEncoder.t18(APP_ID, APP_CLIENT_VERSION, uin),
        TlvEncoder.t1(uin, int(time.time()), IP_BYTES),
        TlvEncoder.t106(
            SSO_VERSION, APP_ID, SUB_APP_ID, APP_CLIENT_VERSION, uin, 0,
            password_md5, DEVICE.guid, DEVICE.tgtgt
        ),
        TlvEncoder.t116(BITMAP, SUB_SIGMAP),
        TlvEncoder.t100(
            SSO_VERSION, APP_ID, SUB_APP_ID, APP_CLIENT_VERSION, MAIN_SIGMAP
        ),
        TlvEncoder.t107(),
        # TlvBuilder.t108(KSID),  # null when first time login
        # TlvBuilder.t104(),
        TlvEncoder.t142(APK_ID),
        TlvEncoder.t144(
            DEVICE.imei.encode(), DEVICE.bootloader, DEVICE.proc_version,
            DEVICE.version.codename, DEVICE.version.incremental,
            DEVICE.fingerprint, DEVICE.boot_id,
            DEVICE.android_id, DEVICE.baseband, DEVICE.version.incremental,
            DEVICE.os_type.encode(),
            DEVICE.version.release.encode(), NETWORK_TYPE, DEVICE.sim.encode(),
            DEVICE.apn.encode(), False, True, False, GUID_FLAG,
            DEVICE.model.encode(), DEVICE.guid, DEVICE.brand.encode(),
            DEVICE.tgtgt
        ),
        TlvEncoder.t145(DEVICE.guid),
        TlvEncoder.t147(APP_ID, APK_VERSION.encode(), APK_SIGN),
        # TlvBuilder.t166(1),
        # TlvBuilder.t16a(),
        TlvEncoder.t154(seq),
        TlvEncoder.t141(DEVICE.sim.encode(), NETWORK_TYPE, DEVICE.apn.encode()),
        TlvEncoder.t8(LOCAL_ID),
        TlvEncoder.t511(
            [
                "tenpay.com", "openmobile.qq.com", "docs.qq.com",
                "connect.qq.com", "qzone.qq.com", "vip.qq.com",
                "gamecenter.qq.com", "qun.qq.com", "game.qq.com",
                "qqweb.qq.com", "office.qq.com", "ti.qq.com", "mail.qq.com",
                "mma.qq.com"
            ]
        ),  # com.tencent.mobileqq.msf.core.auth.l
        # TlvBuilder.t172(),
        # TlvBuilder.t185(1),  # when sms login, is_password_login == 3
        # TlvBuilder.t400(),  # null when first time login
        TlvEncoder.t187(DEVICE.mac_address.encode()),
        TlvEncoder.t188(DEVICE.android_id.encode()),
        TlvEncoder.t194(DEVICE.imsi_md5) if DEVICE.imsi_md5 else b"",
        TlvEncoder.t191(CAN_WEB_VERIFY),
        # TlvBuilder.t201(),
        TlvEncoder.t202(DEVICE.wifi_bssid.encode(), DEVICE.wifi_ssid.encode()),
        TlvEncoder.t177(APK_BUILD_TIME, SDK_VERSION),
        TlvEncoder.t516(),
        TlvEncoder.t521(),
        TlvEncoder.t525(TlvEncoder.t536([])),
        # TlvBuilder.t318()  # not login in by qr
    )
    oicq_packet = OICQRequest.build_encoded(
        uin, COMMAND_ID, ECDH.encrypt(data, key), ECDH.id
    )
    sso_packet = CSsoBodyPacket.build(
        seq, SUB_APP_ID, COMMAND_NAME, DEVICE.imei, session_id, ksid,
        oicq_packet
    )
    # encrypted by 16-byte zero. Reference: `CSSOData::serialize`
    packet = CSsoDataPacket.build(uin, 2, sso_packet, key=bytes(16))
    return packet


# device lock login, when status 204
def encode_login_request20(
    seq: int, key: bytes, session_id: bytes, ksid: bytes, uin: int, t104: bytes,
    g: bytes
):
    """Build device lock login request packet.

    command id: `0x810 = 2064`

    sub command id: `20`

    command name: `wtlogin.login`

    Note:
        Source: oicq.wlogin_sdk.request.p

    Args:
        seq (int): Packet sequence.
        key (bytes): 16 bits key used to decode the response.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        t104 (bytes): T104 response data.
        g (bytes): md5 of (guid + dpwd + t402)

    Returns:
        Packet: Login packet.
    """
    COMMAND_ID = 2064
    SUB_COMMAND_ID = 20
    COMMAND_NAME = "wtlogin.login"

    SUB_APP_ID = APK_INFO.sub_app_id
    BITMAP = APK_INFO.bitmap
    SUB_SIGMAP = APK_INFO.sub_sigmap

    LOCAL_ID = 2052  # oicq.wlogin_sdk.request.t.v

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 4),  # packet num
        TlvEncoder.t8(LOCAL_ID),
        TlvEncoder.t104(t104),
        TlvEncoder.t116(BITMAP, SUB_SIGMAP),
        TlvEncoder.t401(g)
    )
    oicq_packet = OICQRequest.build_encoded(
        uin, COMMAND_ID, ECDH.encrypt(data, key), ECDH.id
    )
    sso_packet = CSsoBodyPacket.build(
        seq, SUB_APP_ID, COMMAND_NAME, DEVICE.imei, session_id, ksid,
        oicq_packet
    )
    # encrypted by 16-byte zero. Reference: `CSSOData::serialize`
    packet = CSsoDataPacket.build(uin, 2, sso_packet, key=bytes(16))
    return packet


def decode_login_response(packet: IncomingPacket) -> OICQResponse:
    return OICQResponse.decode_response(
        packet.uin, packet.seq, packet.ret_code, packet.command_name,
        packet.data
    )


__all__ = [
    "encode_login_request2_captcha", "encode_login_request2_slider",
    "encode_login_request9", "encode_login_request20", "decode_login_response",
    "OICQResponse", "LoginSuccess", "NeedCaptcha", "AccountFrozen",
    "DeviceLocked", "TooManySMSRequest", "DeviceLockLogin", "UnknownLoginStatus"
]
