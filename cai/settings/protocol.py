"""Application Protocol setting

This module is used to get or new the application protocol setting.
Protocol settings will be stored in APP_DIR provided by storage manager.
Once the protocol setting is loaded, it will be cached until application shut down.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import os
from typing import Optional, NamedTuple

from cai.storage import Storage

MISSING = "MISSING"

_protocol: Optional["ApkInfo"] = None


class ApkInfo(NamedTuple):
    apk_id: str
    app_id: int  # com.tencent.common.config.AppSetting.f
    version: str
    build_time: int
    apk_sign: bytes
    sdk_version: str  # oicq.wlogin_sdk.tools.util.SDK_VERSION
    sso_version: int  # oicq.wlogin_sdk.tools.util.SSO_VERSION
    bitmap: int
    sigmap: int
    sub_sigmap: int


ANDROID_PHONE = ApkInfo(
    apk_id="com.tencent.mobileqq",
    app_id=537066738,
    version="8.5.0",
    build_time=1607689988,
    apk_sign=bytes(
        [
            0xA6, 0xB7, 0x45, 0xBF, 0x24, 0xA2, 0xC2, 0x77, 0x52, 0x77, 0x16,
            0xF6, 0xF3, 0x6E, 0xB6, 0x8D
        ]
    ),
    sdk_version="6.0.0.2454",
    sso_version=15,
    bitmap=184024956,
    sigmap=34869472,
    sub_sigmap=0x10400
)
ANDROID_WATCH = ApkInfo(
    apk_id="com.tencent.mobileqq",
    app_id=537061176,
    version="8.2.7",
    build_time=1571193922,
    apk_sign=bytes(
        [
            0xA6, 0xB7, 0x45, 0xBF, 0x24, 0xA2, 0xC2, 0x77, 0x52, 0x77, 0x16,
            0xF6, 0xF3, 0x6E, 0xB6, 0x8D
        ]
    ),
    sdk_version="6.0.0.2413",
    sso_version=5,
    bitmap=184024956,
    sigmap=34869472,
    sub_sigmap=0x10400
)
IPAD = ApkInfo(
    apk_id="com.tencent.minihd.qq",
    app_id=537065739,
    version="5.8.9",
    build_time=1595836208,
    apk_sign=bytes(
        [
            170, 57, 120, 244, 31, 217, 111, 249, 145, 74, 102, 158, 24, 100,
            116, 199
        ]
    ),
    sdk_version="6.0.0.2433",
    sso_version=12,
    bitmap=150470524,
    sigmap=1970400,
    sub_sigmap=66560
)
MACOS = ApkInfo(
    apk_id="com.tencent.minihd.qq",
    app_id=537064315,
    version="5.8.9",
    build_time=1595836208,
    apk_sign=bytes(
        [
            170, 57, 120, 244, 31, 217, 111, 249, 145, 74, 102, 158, 24, 100,
            116, 199
        ]
    ),
    sdk_version="6.0.0.2433",
    sso_version=12,
    bitmap=150470524,
    sigmap=1970400,
    sub_sigmap=66560
)


def get_apk_info(type_: str = "0") -> ApkInfo:
    info = {"0": IPAD, "1": ANDROID_PHONE, "2": ANDROID_WATCH, "3": MACOS}
    if type_ not in info:
        raise ValueError(f"Invalid Protocol Type: {type_}")
    return info[type_]


def get_protocol(cache: bool = True) -> ApkInfo:
    global _protocol
    if cache and _protocol:
        return _protocol

    type_ = os.getenv(Storage.protocol_env_name, MISSING)
    if type_ is MISSING and os.path.exists(Storage.protocol_file):
        with open(Storage.protocol_file, "r") as f:
            type_ = f.read()
    elif type_ is MISSING:
        type_ = "0"
        with open(Storage.protocol_file, "w") as f:
            f.write("0")
    _protocol = get_apk_info(type_)
    return _protocol
