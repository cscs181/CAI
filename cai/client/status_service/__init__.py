"""StatSvc Related SDK

This module is used to build and handle status service related packet.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol

from .jce import SvcReqRegister

DEVICE = get_device()
APK_INFO = get_protocol()


# register
def encode_register(
    seq: int, key: bytes, session_id: bytes, ksid: bytes, uin: int
):
    svc = SvcReqRegister(
        uin=uin,
        bid=7,  # login: 1 | 2 | 4, logout: 0
        status=11,  # login: 11, logout: 21
        ios_version=DEVICE.version.sdk,
        nettype=1,
        reg_type=bytes(1),
        guid=DEVICE.guid,
        locale_id=2052,
        dev_name=DEVICE.model,
        dev_type=DEVICE.model,
        os_version=DEVICE.version.release,
        large_seq=1551,
        old_sso_ip=0,
        new_sso_ip=31806887127679168,
        channel_num="",
        cp_id=0,
        vendor_name=DEVICE.brand,
        vendor_os_name=DEVICE.brand,
        b769=bytes(
            [
                0x0A, 0x04, 0x08, 0x2E, 0x10, 0x00, 0x0A, 0x05, 0x08, 0x9B,
                0x02, 0x10, 0x00
            ]
        ),
        is_set_status=False,
        set_mute=False,
        ext_online_status=1000,
        battery_status=98
    )
