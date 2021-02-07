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
    IP_BYTES = ipaddress.ip_address(DEVICE.ip_address).packed
    APK_ID = APK_INFO.apk_id
    APP_ID = APK_INFO.app_id
    SUB_APP_ID = APK_INFO.sub_app_id
    APP_CLIENT_VERSION = 0
    SSO_VERSION = APK_INFO.sso_version
    BITMAP = APK_INFO.bitmap
    MAIN_SIGMAP = APK_INFO.main_sigmap
    SUB_SIGMAP = APK_INFO.sub_sigmap

    # KSID = f"|{DEVICE.imei}|{APK_INFO.version}"

    data = Packet().write(
        struct.pack(">HH", 9, 24),  # sub command id, packet num
        TlvBuilder.t18(APP_ID, APP_CLIENT_VERSION, uin),
        TlvBuilder.t1(uin, int(time.time()), IP_BYTES),
        TlvBuilder.t106(
            SSO_VERSION, APP_ID, APP_CLIENT_VERSION, uin, 0, IP_BYTES,
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
        TlvBuilder.t144(),
        TlvBuilder.t145(),
        TlvBuilder.t147(),
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
