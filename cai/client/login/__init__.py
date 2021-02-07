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
from cai.utils.binary import Packet
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol

DEVICE = get_device()
APK_INFO = get_protocol()


async def login(uin: int, password: str):
    """Build login request packet.

    command id: `0x810 = 2064`,
    sub command id: `9`
    command name: `wtlogin.login`

    Note:
        Source: oicq.wlogin_sdk.request.k
    """
    APK_ID = APK_INFO.apk_id
    APK_VERSION = APK_INFO.version
    APK_SIGN = APK_INFO.apk_sign
    APP_ID = APK_INFO.app_id
    SUB_APP_ID = APK_INFO.sub_app_id
    APP_CLIENT_VERSION = 0
    SSO_VERSION = APK_INFO.sso_version
    BITMAP = APK_INFO.bitmap
    MAIN_SIGMAP = APK_INFO.main_sigmap
    SUB_SIGMAP = APK_INFO.sub_sigmap

    # KSID = f"|{DEVICE.imei}|{APK_INFO.version}"
    GUID_FLAG = 0
    GUID_FLAG |= 1 << 24 & 0xFF000000
    GUID_FLAG |= 0 << 8 & 0xFF00
    IP_BYTES = ipaddress.ip_address(DEVICE.ip_address).packed

    data = Packet().write(
        struct.pack(">HH", 9, 24),  # sub command id, packet num
        TlvBuilder.t18(APP_ID, APP_CLIENT_VERSION, uin),
        TlvBuilder.t1(uin, int(time.time()), IP_BYTES),
        TlvBuilder.t106(
            SSO_VERSION, APP_ID, SUB_APP_ID, APP_CLIENT_VERSION, uin, 0,
            IP_BYTES,
            md5(password.encode()).digest(), True, DEVICE.guid, DEVICE.tgtgt
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
            DEVICE.os_type.encode(), DEVICE.version.release.encode(),
            DEVICE.sim.encode(), DEVICE.apn.encode(), False, True,
            False, GUID_FLAG, DEVICE.model.encode(), DEVICE.guid,
            DEVICE.brand.encode(), DEVICE.tgtgt
        ),
        TlvBuilder.t145(DEVICE.guid),
        TlvBuilder.t147(APP_ID, APK_VERSION.encode(), APK_SIGN),
        TlvBuilder.t154(),
        TlvBuilder.t141(),
        TlvBuilder.t8(),
        TlvBuilder.t511(),
        TlvBuilder.t187(),
        TlvBuilder.t188(),
        TlvBuilder.t194(),
        TlvBuilder.t191(),
        TlvBuilder.t202(),
        TlvBuilder.t177(),
        TlvBuilder.t516(),
        TlvBuilder.t521(),
        TlvBuilder.t525(),
    )
