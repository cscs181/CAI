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
from hashlib import md5

from .tlv import TlvBuilder
from cai.utils.ecdh import ECDH
from cai.utils.binary import Packet
from .oicq_packet import OICQRequest
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol
from cai.client.packet import SsoPacket, LoginPacket

DEVICE = get_device()
APK_INFO = get_protocol()


async def login(
    seq: int, key: bytes, session_id: bytes, uin: int, password_md5: bytes
):
    """Build login request packet.

    command id: `0x810 = 2064`,
    sub command id: `9`
    command name: `wtlogin.login`

    Note:
        Source: oicq.wlogin_sdk.request.k

    Args:
        seq (int): Packet sequence.
        key (bytes): 16 bits key used to decode the response.
        session_id (bytes): Session ID
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

    GUID_FLAG = 0
    GUID_FLAG |= 1 << 24 & 0xFF000000
    GUID_FLAG |= 0 << 8 & 0xFF00
    CAN_WEB_VERIFY = 130  # oicq.wlogin_sdk.request.k.K
    LOCAL_ID = 2052  # com.tencent.qqmini.minigame.GameConst.GAME_RUNTIME_MSG_GAME_ON_HIDE
    IP_BYTES = ipaddress.ip_address(DEVICE.ip_address).packed
    NETWORK_TYPE = (DEVICE.apn == "wifi") + 1
    KSID = f"|{DEVICE.imei}|A8.2.7.27f6ea96".encode()

    data = Packet.build(
        struct.pack(">HH", SUB_COMMAND_ID, 23),  # packet num
        TlvBuilder.t18(APP_ID, APP_CLIENT_VERSION, uin),
        TlvBuilder.t1(uin, int(time.time()), IP_BYTES),
        TlvBuilder.t106(
            SSO_VERSION, APP_ID, SUB_APP_ID, APP_CLIENT_VERSION, uin, 0,
            IP_BYTES, password_md5, True, DEVICE.guid, DEVICE.tgtgt
        ),
        TlvBuilder.t116(BITMAP, SUB_SIGMAP),
        TlvBuilder.t100(
            SSO_VERSION, APP_ID, SUB_APP_ID, APP_CLIENT_VERSION, MAIN_SIGMAP
        ),
        TlvBuilder.t107(),
        # TlvBuilder.t108(KSID),  # null when first time login
        # TlvBuilder.t104(),
        TlvBuilder.t142(APK_ID),
        TlvBuilder.t144(
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
        TlvBuilder.t145(DEVICE.guid),
        TlvBuilder.t147(APP_ID, APK_VERSION.encode(), APK_SIGN),
        # TlvBuilder.t166(1),
        # TlvBuilder.t16a(),
        TlvBuilder.t154(seq),
        TlvBuilder.t141(DEVICE.sim.encode(), NETWORK_TYPE, DEVICE.apn.encode()),
        TlvBuilder.t8(LOCAL_ID),
        TlvBuilder.t511(
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
        TlvBuilder.t187(DEVICE.mac_address.encode()),
        TlvBuilder.t188(DEVICE.android_id.encode()),
        TlvBuilder.t194(DEVICE.imsi_md5) if DEVICE.imsi_md5 else b"",
        TlvBuilder.t191(CAN_WEB_VERIFY),
        # TlvBuilder.t201(),
        TlvBuilder.t202(DEVICE.wifi_bssid.encode(), DEVICE.wifi_ssid.encode()),
        TlvBuilder.t177(APK_BUILD_TIME, SDK_VERSION),
        TlvBuilder.t516(),
        TlvBuilder.t521(),
        TlvBuilder.t525(TlvBuilder.t536(bytes([1, 0]))),  # 1, length
        # TlvBuilder.t318()  # not login in by qr
    )
    oicq_packet = OICQRequest.build_encoded(
        uin, COMMAND_ID, ECDH.encrypt(data, key), ECDH.id
    )
    sso_packet = SsoPacket.build(
        seq, SUB_APP_ID, COMMAND_NAME, DEVICE.imei, session_id, KSID,
        oicq_packet
    )
    packet = LoginPacket.build(uin, 2, sso_packet, bytes(16))
    return packet
