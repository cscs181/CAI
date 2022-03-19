"""Login Related SDK

This module is used to build and handle login related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import ipaddress
import secrets
import string
import struct
import time
from hashlib import md5
from typing import TYPE_CHECKING, Tuple

from rtea import qqtea_decrypt

from cai.client.packet import (
    UniPacket,
    CSsoBodyPacket,
    CSsoDataPacket,
    IncomingPacket,
)
from cai.settings.device import DeviceInfo
from cai.settings.protocol import ApkInfo
from cai.utils.binary import Packet
from cai.utils.crypto import ECDH, EncryptSession
from .oicq import (
    NeedCaptcha,
    OICQRequest,
    DeviceLocked,
    LoginSuccess,
    OICQResponse,
    AccountFrozen,
    DeviceLockLogin,
    TooManySMSRequest,
    UnknownLoginStatus,
)
from .tlv import TlvEncoder

if TYPE_CHECKING:
    from cai.client import Client


# submit captcha
def encode_login_request2_captcha(
    seq: int,
    key: bytes,
    session_id: bytes,
    ksid: bytes,
    uin: int,
    captcha: str,
    sign: bytes,
    t104: bytes,
    imei: str,
    apk_info: ApkInfo
) -> Packet:
    """Build submit captcha request packet.

    Called in ``oicq.wlogin_sdk.request.WtloginHelper.CheckPictureAndGetSt``.

    command id: ``0x810 = 2064``

    sub command id: ``2``

    command name: ``wtlogin.login``

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
        apk_info (ApkInfo): ApkInfo
        imei (str): device imei

    Returns:
        Packet: Login packet.
    """
    COMMAND_ID = 2064
    SUB_COMMAND_ID = 2
    COMMAND_NAME = "wtlogin.login"

    SUB_APP_ID = apk_info.sub_app_id
    BITMAP = apk_info.bitmap
    SUB_SIGMAP = apk_info.sub_sigmap

    LOCAL_ID = 2052  # oicq.wlogin_sdk.request.t.v

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 4),  # packet num
        TlvEncoder.t2(captcha.encode(), sign),
        TlvEncoder.t8(LOCAL_ID),
        TlvEncoder.t104(t104),
        TlvEncoder.t116(BITMAP, SUB_SIGMAP),
    )
    oicq_packet = OICQRequest.build_encoded(
        uin, COMMAND_ID, ECDH.encrypt(data, key), ECDH.id
    )
    sso_packet = CSsoBodyPacket.build(
        seq,
        SUB_APP_ID,
        COMMAND_NAME,
        imei,
        session_id,
        ksid,
        oicq_packet,
    )
    # encrypted by 16-byte zero. Reference: ``CSSOData::serialize``
    packet = CSsoDataPacket.build(uin, 2, sso_packet, key=bytes(16))
    return packet


# submit ticket
def encode_login_request2_slider(
    seq: int,
    key: bytes,
    session_id: bytes,
    ksid: bytes,
    uin: int,
    ticket: str,
    t104: bytes,
    imei: str,
    apk_info: ApkInfo
) -> Packet:
    """Build slider ticket request packet.

    Called in ``oicq.wlogin_sdk.request.WtloginHelper.CheckPictureAndGetSt``.

    command id: ``0x810 = 2064``

    sub command id: ``2``

    command name: ``wtlogin.login``

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
        apk_info (ApkInfo): ApkInfo
        imei (str): device imei

    Returns:
        Packet: Login packet.
    """
    COMMAND_ID = 2064
    SUB_COMMAND_ID = 2
    COMMAND_NAME = "wtlogin.login"

    SUB_APP_ID = apk_info.sub_app_id
    BITMAP = apk_info.bitmap
    SUB_SIGMAP = apk_info.sub_sigmap

    LOCAL_ID = 2052  # oicq.wlogin_sdk.request.t.v

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 4),  # packet num
        TlvEncoder.t193(ticket),
        TlvEncoder.t8(LOCAL_ID),
        TlvEncoder.t104(t104),
        TlvEncoder.t116(BITMAP, SUB_SIGMAP),
    )
    oicq_packet = OICQRequest.build_encoded(
        uin, COMMAND_ID, ECDH.encrypt(data, key), ECDH.id
    )
    sso_packet = CSsoBodyPacket.build(
        seq,
        SUB_APP_ID,
        COMMAND_NAME,
        imei,
        session_id,
        ksid,
        oicq_packet,
    )
    # encrypted by 16-byte zero. Reference: ``CSSOData::serialize``
    packet = CSsoDataPacket.build(uin, 2, sso_packet, key=bytes(16))
    return packet


# submit sms
def encode_login_request7(
    seq: int,
    key: bytes,
    session_id: bytes,
    ksid: bytes,
    uin: int,
    sms_code: str,
    t104: bytes,
    t174: bytes,
    g: bytes,
    imei: str,
    apk_info: ApkInfo
) -> Packet:
    """Build sms submit packet.

    Called in ``oicq.wlogin_sdk.request.WtloginHelper.CheckSMSAndGetSt``.

    command id: ``0x810 = 2064``

    sub command id: ``7``

    command name: ``wtlogin.login``

    Note:
        Source: oicq.wlogin_sdk.request.o

    Args:
        seq (int): Packet sequence.
        key (bytes): 16 bits key used to decode the response.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        sms_code (str): SMS code.
        t104 (bytes): TLV 104 data.
        t174 (bytes): TLV 174 data.
        g (bytes): G data of client.
        apk_info (ApkInfo): ApkInfo
        imei (str): device imei

    Returns:
        Packet: Login packet.
    """
    COMMAND_ID = 2064
    SUB_COMMAND_ID = 7
    COMMAND_NAME = "wtlogin.login"

    SUB_APP_ID = apk_info.sub_app_id
    BITMAP = apk_info.bitmap
    SUB_SIGMAP = apk_info.sub_sigmap

    GUID_SRC = 1
    GUID_CHANGE = 0
    GUID_FLAG = 0
    GUID_FLAG |= GUID_SRC << 24 & 0xFF000000
    GUID_FLAG |= GUID_CHANGE << 8 & 0xFF00
    LOCAL_ID = 2052  # oicq.wlogin_sdk.request.t.v

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 7),  # packet num
        TlvEncoder.t8(LOCAL_ID),
        TlvEncoder.t104(t104),
        TlvEncoder.t116(BITMAP, SUB_SIGMAP),
        TlvEncoder.t174(t174),
        TlvEncoder.t17c(sms_code),
        TlvEncoder.t401(g),
        TlvEncoder.t198(),
    )
    oicq_packet = OICQRequest.build_encoded(
        uin, COMMAND_ID, ECDH.encrypt(data, key), ECDH.id
    )
    sso_packet = CSsoBodyPacket.build(
        seq,
        SUB_APP_ID,
        COMMAND_NAME,
        imei,
        session_id,
        ksid,
        oicq_packet,
    )
    # encrypted by 16-byte zero. Reference: ``CSSOData::serialize``
    packet = CSsoDataPacket.build(uin, 2, sso_packet, key=bytes(16))
    return packet


# request sms
def encode_login_request8(
    seq: int,
    key: bytes,
    session_id: bytes,
    ksid: bytes,
    uin: int,
    t104: bytes,
    t174: bytes,
    imei: str,
    apk_info: ApkInfo
) -> Packet:
    """Build sms request packet.

    Called in ``oicq.wlogin_sdk.request.WtloginHelper.RefreshSMSData``.

    command id: ``0x810 = 2064``

    sub command id: ``8``

    command name: ``wtlogin.login``

    Note:
        Source: oicq.wlogin_sdk.request.r

    Args:
        seq (int): Packet sequence.
        key (bytes): 16 bits key used to decode the response.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        t104 (bytes): TLV 104 data.
        t174 (bytes): TLV 174 data.
        apk_info (ApkInfo): ApkInfo
        imei (str): device imei

    Returns:
        Packet: Login packet.
    """
    COMMAND_ID = 2064
    SUB_COMMAND_ID = 8
    COMMAND_NAME = "wtlogin.login"

    SMS_APP_ID = 9
    SUB_APP_ID = apk_info.sub_app_id
    BITMAP = apk_info.bitmap
    SUB_SIGMAP = apk_info.sub_sigmap

    GUID_SRC = 1
    GUID_CHANGE = 0
    GUID_FLAG = 0
    GUID_FLAG |= GUID_SRC << 24 & 0xFF000000
    GUID_FLAG |= GUID_CHANGE << 8 & 0xFF00
    LOCAL_ID = 2052  # oicq.wlogin_sdk.request.t.v

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 6),  # packet num
        TlvEncoder.t8(LOCAL_ID),
        TlvEncoder.t104(t104),
        TlvEncoder.t116(BITMAP, SUB_SIGMAP),
        TlvEncoder.t174(t174),
        TlvEncoder.t17a(SMS_APP_ID),
        TlvEncoder.t197(),
    )
    oicq_packet = OICQRequest.build_encoded(
        uin, COMMAND_ID, ECDH.encrypt(data, key), ECDH.id
    )
    sso_packet = CSsoBodyPacket.build(
        seq,
        SUB_APP_ID,
        COMMAND_NAME,
        imei,
        session_id,
        ksid,
        oicq_packet,
    )
    # encrypted by 16-byte zero. Reference: ``CSSOData::serialize``
    packet = CSsoDataPacket.build(uin, 2, sso_packet, key=bytes(16))
    return packet


# password md5 login
def encode_login_request9(
    seq: int,
    key: bytes,
    session_id: bytes,
    ksid: bytes,
    uin: int,
    password_md5: bytes,
    device: DeviceInfo,
    apk_info: ApkInfo
) -> Packet:
    """Build main login request packet.

    Called in ``oicq.wlogin_sdk.request.WtloginHelper.GetStWithPasswd``.

    command id: ``0x810 = 2064``

    sub command id: ``9``

    command name: ``wtlogin.login``

    Note:
        Source: oicq.wlogin_sdk.request.k

    Args:
        seq (int): Packet sequence.
        key (bytes): 16 bits key used to decode the response.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        password_md5 (bytes): User QQ password md5 hash.
        device (DeviceInfo): your device info
        apk_info (ApkInfo): ApkInfo

    Returns:
        Packet: Login packet.
    """
    COMMAND_ID = 2064
    SUB_COMMAND_ID = 9
    COMMAND_NAME = "wtlogin.login"

    APK_ID = apk_info.apk_id
    APK_VERSION = apk_info.version
    APK_SIGN = apk_info.apk_sign
    APK_BUILD_TIME = apk_info.build_time
    APP_ID = apk_info.app_id
    SUB_APP_ID = apk_info.sub_app_id
    APP_CLIENT_VERSION = 0
    SDK_VERSION = apk_info.sdk_version
    SSO_VERSION = apk_info.sso_version
    BITMAP = apk_info.bitmap
    MAIN_SIGMAP = apk_info.main_sigmap
    SUB_SIGMAP = apk_info.sub_sigmap

    GUID_SRC = 1
    GUID_CHANGE = 0
    GUID_FLAG = 0
    GUID_FLAG |= GUID_SRC << 24 & 0xFF000000
    GUID_FLAG |= GUID_CHANGE << 8 & 0xFF00
    CAN_WEB_VERIFY = 130  # oicq.wlogin_sdk.request.k.K
    LOCAL_ID = 2052  # oicq.wlogin_sdk.request.t.v
    IP_BYTES: bytes = ipaddress.ip_address(device.ip_address).packed
    NETWORK_TYPE = (device.apn == "wifi") + 1

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 23),  # packet num
        TlvEncoder.t18(APP_ID, APP_CLIENT_VERSION, uin),
        TlvEncoder.t1(uin, int(time.time()), IP_BYTES),
        TlvEncoder.t106(
            SSO_VERSION,
            APP_ID,
            SUB_APP_ID,
            APP_CLIENT_VERSION,
            uin,
            0,
            password_md5,
            device.guid,
            device.tgtgt,
        ),
        TlvEncoder.t116(BITMAP, SUB_SIGMAP),
        TlvEncoder.t100(
            SSO_VERSION, APP_ID, SUB_APP_ID, APP_CLIENT_VERSION, MAIN_SIGMAP
        ),
        TlvEncoder.t107(),
        # TlvEncoder.t108(KSID),  # null when first time login
        # TlvEncoder.t104(),
        TlvEncoder.t142(APK_ID),
        TlvEncoder.t144(
            device.imei.encode(),
            device.bootloader,
            device.proc_version,
            device.version.codename,
            device.version.incremental,
            device.fingerprint,
            device.boot_id,
            device.android_id,
            device.baseband,
            device.version.incremental,
            device.os_type.encode(),
            device.version.release.encode(),
            NETWORK_TYPE,
            device.sim.encode(),
            device.apn.encode(),
            False,
            True,
            False,
            GUID_FLAG,
            device.model.encode(),
            device.guid,
            device.brand.encode(),
            device.tgtgt,
        ),
        TlvEncoder.t145(device.guid),
        TlvEncoder.t147(APP_ID, APK_VERSION.encode(), APK_SIGN),
        # TlvEncoder.t166(1),
        # TlvEncoder.t16a(),
        TlvEncoder.t154(seq),
        TlvEncoder.t141(device.sim.encode(), NETWORK_TYPE, device.apn.encode()),
        TlvEncoder.t8(LOCAL_ID),
        TlvEncoder.t511(
            [
                "tenpay.com",
                "openmobile.qq.com",
                "docs.qq.com",
                "connect.qq.com",
                "qzone.qq.com",
                "vip.qq.com",
                "gamecenter.qq.com",
                "qun.qq.com",
                "game.qq.com",
                "qqweb.qq.com",
                "office.qq.com",
                "ti.qq.com",
                "mail.qq.com",
                "mma.qq.com",
            ]
        ),  # com.tencent.mobileqq.msf.core.auth.l
        # TlvEncoder.t172(),
        # TlvEncoder.t185(1),  # when sms login, is_password_login == 3
        # TlvEncoder.t400(),  # null when first time login
        TlvEncoder.t187(device.mac_address.encode()),
        TlvEncoder.t188(device.android_id.encode()),
        TlvEncoder.t194(device.imsi_md5) if device.imsi_md5 else b"",
        TlvEncoder.t191(CAN_WEB_VERIFY),
        # TlvEncoder.t201(),
        TlvEncoder.t202(device.wifi_bssid.encode(), device.wifi_ssid.encode()),
        TlvEncoder.t177(APK_BUILD_TIME, SDK_VERSION),
        TlvEncoder.t516(),
        TlvEncoder.t521(),
        TlvEncoder.t525(TlvEncoder.t536([])),
        # TlvEncoder.t318()  # not login in by qr
    )
    oicq_packet = OICQRequest.build_encoded(
        uin, COMMAND_ID, ECDH.encrypt(data, key), ECDH.id
    )
    sso_packet = CSsoBodyPacket.build(
        seq,
        SUB_APP_ID,
        COMMAND_NAME,
        device.imei,
        session_id,
        ksid,
        oicq_packet,
    )
    # encrypted by 16-byte zero. Reference: ``CSSOData::serialize``
    packet = CSsoDataPacket.build(uin, 2, sso_packet, key=bytes(16))
    return packet


# device lock login, when status 204
def encode_login_request20(
    seq: int,
    key: bytes,
    session_id: bytes,
    ksid: bytes,
    uin: int,
    t104: bytes,
    g: bytes,
    imei: str,
    apk_info: ApkInfo
) -> Packet:
    """Build device lock login request packet.

    Called in ``oicq.wlogin_sdk.request.WtloginHelper.GetStWithoutPasswd``.

    command id: ``0x810 = 2064``

    sub command id: ``20``

    command name: ``wtlogin.login``

    Note:
        Source: oicq.wlogin_sdk.request.p

    Args:
        seq (int): Packet sequence.
        key (bytes): 16 bits key used to decode the response.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        t104 (bytes): T104 response data.
        g (bytes): md5 of (guid + dpwd + t402).
        imei (str): device imei
        apk_info (ApkInfo): ApkInfo

    Returns:
        Packet: Login packet.
    """
    COMMAND_ID = 2064
    SUB_COMMAND_ID = 20
    COMMAND_NAME = "wtlogin.login"

    SUB_APP_ID = apk_info.sub_app_id
    BITMAP = apk_info.bitmap
    SUB_SIGMAP = apk_info.sub_sigmap

    LOCAL_ID = 2052  # oicq.wlogin_sdk.request.t.v

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 4),  # packet num
        TlvEncoder.t8(LOCAL_ID),
        TlvEncoder.t104(t104),
        TlvEncoder.t116(BITMAP, SUB_SIGMAP),
        TlvEncoder.t401(g),
    )
    oicq_packet = OICQRequest.build_encoded(
        uin, COMMAND_ID, ECDH.encrypt(data, key), ECDH.id
    )
    sso_packet = CSsoBodyPacket.build(
        seq,
        SUB_APP_ID,
        COMMAND_NAME,
        imei,
        session_id,
        ksid,
        oicq_packet,
    )
    # encrypted by 16-byte zero. Reference: ``CSSOData::serialize``
    packet = CSsoDataPacket.build(uin, 2, sso_packet, key=bytes(16))
    return packet


# TODO: fast refresh
# refresh siginfo by A2
def encode_exchange_emp_10() -> Packet:
    ...


# refresh siginfo by A1
def encode_exchange_emp_15(
    seq: int,
    session_id: bytes,
    uin: int,
    g: bytes,
    dpwd: bytes,
    no_pic_sig: bytes,
    encrypted_a1: bytes,
    rand_seed: bytes,
    wt_session_ticket: bytes,
    wt_session_ticket_key: bytes,
    device: DeviceInfo,
    apk_info: ApkInfo
) -> Packet:
    """Build exchange emp request packet.

    command id: ``0x810 = 2064``

    sub command id: ``15``

    command name: ``wtlogin.exchange_emp``

    Note:
        Source: oicq.wlogin_sdk.request.aa

    Args:
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        g (bytes): Siginfo g.
        dpwd (bytes): Siginfo dpwd.
        no_pic_sig (bytes): Siginfo no pic sig.
        encrypted_a1 (bytes): Siginfo Encrypted A1.
        rand_seed (bytes): Siginfo random seed.
        wt_session_ticket (bytes): Siginfo session ticket.
        wt_session_ticket_key (bytes): Siginfo session ticket key.
        device (DeviceInfo): your device info
        apk_info (ApkInfo): ApkInfo

    Returns:
        Packet: Exchange emp packet.
    """
    COMMAND_ID = 2064
    SUB_COMMAND_ID = 15
    COMMAND_NAME = "wtlogin.exchange_emp"

    APK_ID = apk_info.apk_id
    APK_VERSION = apk_info.version
    APK_SIGN = apk_info.apk_sign
    APK_BUILD_TIME = apk_info.build_time
    APP_ID = apk_info.app_id
    SUB_APP_ID = apk_info.sub_app_id
    APP_CLIENT_VERSION = 0
    SDK_VERSION = apk_info.sdk_version
    SSO_VERSION = apk_info.sso_version
    BITMAP = apk_info.bitmap
    MAIN_SIGMAP = apk_info.main_sigmap
    SUB_SIGMAP = apk_info.sub_sigmap

    GUID = device.guid
    GUID_SRC = 1
    GUID_CHANGE = 0
    GUID_FLAG = 0
    GUID_FLAG |= GUID_SRC << 24 & 0xFF000000
    GUID_FLAG |= GUID_CHANGE << 8 & 0xFF00
    LOCAL_ID = 2052  # oicq.wlogin_sdk.request.t.v
    IP_BYTES: bytes = ipaddress.ip_address(device.ip_address).packed
    NETWORK_TYPE = (device.apn == "wifi") + 1

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 24),
        TlvEncoder.t18(APP_ID, APP_CLIENT_VERSION, uin),
        TlvEncoder.t1(uin, int(time.time()), IP_BYTES),
        TlvEncoder._pack_tlv(0x106, encrypted_a1),
        TlvEncoder.t116(BITMAP, SUB_SIGMAP),
        TlvEncoder.t100(
            SSO_VERSION, APP_ID, SUB_APP_ID, APP_CLIENT_VERSION, MAIN_SIGMAP
        ),
        TlvEncoder.t107(),
        # TlvEncoder.t108(KSID),  # null when first time login
        TlvEncoder.t144(
            device.imei.encode(),
            device.bootloader,
            device.proc_version,
            device.version.codename,
            device.version.incremental,
            device.fingerprint,
            device.boot_id,
            device.android_id,
            device.baseband,
            device.version.incremental,
            device.os_type.encode(),
            device.version.release.encode(),
            NETWORK_TYPE,
            device.sim.encode(),
            device.apn.encode(),
            False,
            True,
            False,
            GUID_FLAG,
            device.model.encode(),
            device.guid,
            device.brand.encode(),
            device.tgtgt,
        ),
        TlvEncoder.t142(APK_ID),
        # TlvEncoder.t112(),
        TlvEncoder.t145(device.guid),
        # TlvEncoder.t166(1),
        TlvEncoder.t16a(no_pic_sig),
        TlvEncoder.t154(seq),
        TlvEncoder.t141(device.sim.encode(), NETWORK_TYPE, device.apn.encode()),
        TlvEncoder.t8(LOCAL_ID),
        TlvEncoder.t511(
            [
                "tenpay.com",
                "openmobile.qq.com",
                "docs.qq.com",
                "connect.qq.com",
                "qzone.qq.com",
                "vip.qq.com",
                "gamecenter.qq.com",
                "qun.qq.com",
                "game.qq.com",
                "qqweb.qq.com",
                "office.qq.com",
                "ti.qq.com",
                "mail.qq.com",
                "mma.qq.com",
            ]
        ),  # com.tencent.mobileqq.msf.core.auth.l
        TlvEncoder.t147(APP_ID, APK_VERSION.encode(), APK_SIGN),
        # TlvEncoder.t172(),
        TlvEncoder.t177(APK_BUILD_TIME, SDK_VERSION),
        TlvEncoder.t400(g, uin, GUID, dpwd, 1, APP_ID, rand_seed),
        TlvEncoder.t187(device.mac_address.encode()),
        TlvEncoder.t188(device.android_id.encode()),
        TlvEncoder.t194(device.imsi_md5) if device.imsi_md5 else b"",
        # TlvEncoder.t201(),
        TlvEncoder.t202(device.wifi_bssid.encode(), device.wifi_ssid.encode()),
        TlvEncoder.t516(),
        TlvEncoder.t521(),
        TlvEncoder.t525(TlvEncoder.t536([])),
    )
    session = EncryptSession(wt_session_ticket)
    oicq_packet = OICQRequest.build_encoded(
        uin,
        COMMAND_ID,
        session.encrypt(data, wt_session_ticket_key),
        session.id,
    )
    packet = UniPacket.build(
        uin, seq, COMMAND_NAME, session_id, 2, oicq_packet, key=bytes(16)
    )
    return packet


async def handle_oicq_response(
    client: "Client", packet: IncomingPacket, dev: Tuple[DeviceInfo, ApkInfo]
) -> OICQResponse:
    device, apk_info = dev

    response = OICQResponse.decode_response(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
        device.tgtgt
    )
    if not isinstance(response, UnknownLoginStatus):
        return response

    if response.t402:
        client._siginfo.dpwd = (
            "".join(
                secrets.choice(string.ascii_letters + string.digits)
                for _ in range(16)
            )
        ).encode()
        client._t402 = response.t402
        client._siginfo.g = md5(
            device.guid + client._siginfo.dpwd + client._t402
        ).digest()

    if isinstance(response, LoginSuccess):
        client._t150 = response.t150 or client._t150
        client._rollback_sig = response.rollback_sig or client._rollback_sig
        client._time_diff = response.time_diff or client._time_diff
        client._ip_address = response.ip_address or client._ip_address
        client._t528 = response.t528 or client._t528
        client._t530 = response.t530 or client._t530
        client._ksid = response.ksid or client._ksid
        client._pwd_flag = response.pwd_flag or client._pwd_flag
        client._nick = response.nick or client._nick
        client._age = response.age or client._age
        client._gender = response.gender or client._gender

        client._siginfo.d2 = response.d2 or client._siginfo.d2
        client._siginfo.d2key = response.d2key or client._siginfo.d2key
        client._siginfo.tgt = response.tgt or client._siginfo.tgt
        client._siginfo.tgt_key = response.tgt_key or client._siginfo.tgt_key
        client._siginfo.device_token = (
            response.device_token or client._siginfo.device_token
        )
        client._siginfo.no_pic_sig = (
            response.no_pic_sig or client._siginfo.no_pic_sig
        )
        client._siginfo.encrypted_a1 = (
            response.encrypted_a1 or client._siginfo.encrypted_a1
        )
        client._siginfo.ps_key_map = (
            response.ps_key_map or client._siginfo.ps_key_map
        )
        client._siginfo.pt4_token_map = (
            response.pt4_token_map or client._siginfo.pt4_token_map
        )
        client._siginfo.rand_seed = (
            response.rand_seed or client._siginfo.rand_seed
        )
        client._siginfo.s_key = response.s_key or client._siginfo.s_key
        client._siginfo.user_st_key = (
            response.user_st_key or client._siginfo.user_st_key
        )
        client._siginfo.user_st_web_sig = (
            response.user_st_web_sig or client._siginfo.user_st_web_sig
        )
        client._siginfo.wt_session_ticket = (
            response.wt_session_ticket or client._siginfo.wt_session_ticket
        )
        client._siginfo.wt_session_ticket_key = (
            response.wt_session_ticket_key
            or client._siginfo.wt_session_ticket_key
        )

        key = md5(
            client._password_md5 + bytes(4) + struct.pack(">I", client._uin)
        ).digest()
        decrypted = qqtea_decrypt(response.encrypted_a1, key)
        device.tgtgt = decrypted[51:67]
    elif isinstance(response, NeedCaptcha):
        client._t104 = response.t104 or client._t104
    elif isinstance(response, DeviceLocked):
        client._t104 = response.t104 or client._t104
        client._t174 = response.t174 or client._t174
        client._siginfo.rand_seed = (
            response.rand_seed or client._siginfo.rand_seed
        )
    elif isinstance(response, DeviceLockLogin):
        client._t104 = response.t104 or client._t104
        client._siginfo.rand_seed = (
            response.rand_seed or client._siginfo.rand_seed
        )
    return response


__all__ = [
    "encode_login_request2_captcha",
    "encode_login_request2_slider",
    "encode_login_request9",
    "encode_login_request20",
    "encode_exchange_emp_10",
    "encode_exchange_emp_15",
    "handle_oicq_response",
    "OICQResponse",
    "LoginSuccess",
    "NeedCaptcha",
    "AccountFrozen",
    "DeviceLocked",
    "TooManySMSRequest",
    "DeviceLockLogin",
    "UnknownLoginStatus",
]
