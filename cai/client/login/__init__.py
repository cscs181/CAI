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

from .tlv import TlvBuilder
from cai.utils.binary import Packet
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol


async def login(uin: int):
    """Build login request packet.

    command id: `0x810 = 2064`,
    sub command id: `9`
    command name: `wtlogin.login`

    Note:
        Source: oicq.wlogin_sdk.request.k
    """
    DEVICE = get_device()
    APK_INFO = get_protocol()
    IP_BYTES = ipaddress.ip_address(DEVICE.ip_address).packed
    APP_ID = 16
    APP_CLIENT_VERSION = 0

    data = Packet().write(
        struct.pack(">HH", 9, 24),  # sub command id, packet num
        TlvBuilder.t18(APP_ID, APP_CLIENT_VERSION, uin),
        TlvBuilder.t1(uin, int(time.time()), IP_BYTES),
        TlvBuilder.t106(
            APK_INFO.sso_version, APP_ID, APP_CLIENT_VERSION, uin, 0, IP_BYTES
        ),
        TlvBuilder.t116(),
        TlvBuilder.t100(),
        TlvBuilder.t107(),
        TlvBuilder.t108(),
        TlvBuilder.t142(),
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
