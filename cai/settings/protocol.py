"""Application Protocol setting

This module is used to get or new the application protocol setting.
Protocol settings will be stored in APP_DIR provided by storage manager.
Once the protocol setting is loaded, it will be cached until application shut down.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
from typing import NamedTuple

from cai.storage import Storage


class ApkInfo(NamedTuple):
    apk_id: str
    app_id: int
    sub_app_id: int  # com.tencent.common.config.AppSetting.f
    version: str
    apk_sign: bytes
    build_time: int  # oicq.wlogin_sdk.tools.util.BUILD_TIME
    sdk_version: str  # oicq.wlogin_sdk.tools.util.SDK_VERSION
    sso_version: int  # oicq.wlogin_sdk.tools.util.SSO_VERSION
    bitmap: int  # oicq.wlogin_sdk.request.WtloginHelper.mMiscBitmap | 0x2000000
    main_sigmap: int  # com.tencent.mobileqq.msf.core.auth.n.f
    sub_sigmap: int  # oicq.wlogin_sdk.request.WtloginHelper.mSubSigMap


ANDROID_PHONE = ApkInfo(
    apk_id="com.tencent.mobileqq",
    app_id=16,
    sub_app_id=537066738,
    version="8.5.0",
    build_time=1607689988,
    apk_sign=bytes(
        [
            0xA6,
            0xB7,
            0x45,
            0xBF,
            0x24,
            0xA2,
            0xC2,
            0x77,
            0x52,
            0x77,
            0x16,
            0xF6,
            0xF3,
            0x6E,
            0xB6,
            0x8D,
        ]
    ),
    sdk_version="6.0.0.2454",
    sso_version=15,
    bitmap=184024956,
    main_sigmap=34869472,
    sub_sigmap=0x10400,
)
ANDROID_WATCH = ApkInfo(
    apk_id="com.tencent.mobileqq",
    app_id=16,
    sub_app_id=537061176,
    version="8.2.7",
    build_time=1571193922,
    apk_sign=bytes(
        [
            0xA6,
            0xB7,
            0x45,
            0xBF,
            0x24,
            0xA2,
            0xC2,
            0x77,
            0x52,
            0x77,
            0x16,
            0xF6,
            0xF3,
            0x6E,
            0xB6,
            0x8D,
        ]
    ),
    sdk_version="6.0.0.2413",
    sso_version=5,
    bitmap=184024956,
    main_sigmap=34869472,
    sub_sigmap=0x10400,
)
IPAD = ApkInfo(
    apk_id="com.tencent.minihd.qq",
    app_id=16,
    sub_app_id=537065739,
    version="5.8.9",
    build_time=1595836208,
    apk_sign=bytes(
        [
            170,
            57,
            120,
            244,
            31,
            217,
            111,
            249,
            145,
            74,
            102,
            158,
            24,
            100,
            116,
            199,
        ]
    ),
    sdk_version="6.0.0.2433",
    sso_version=12,
    bitmap=150470524,
    main_sigmap=1970400,
    sub_sigmap=66560,
)
MACOS = ApkInfo(
    apk_id="com.tencent.minihd.qq",
    app_id=16,
    sub_app_id=537064315,
    version="5.8.9",
    build_time=1595836208,
    apk_sign=bytes(
        [
            170,
            57,
            120,
            244,
            31,
            217,
            111,
            249,
            145,
            74,
            102,
            158,
            24,
            100,
            116,
            199,
        ]
    ),
    sdk_version="6.0.0.2433",
    sso_version=12,
    bitmap=150470524,
    main_sigmap=1970400,
    sub_sigmap=66560,
)


def get_apk_info(_type: str = "IPAD") -> ApkInfo:
    info = {
        "IPAD": IPAD,
        "ANDROID_PHONE": ANDROID_PHONE,
        "ANDROID_WATCH": ANDROID_WATCH,
        "MACOS": MACOS,
    }
    if _type not in info:
        raise ValueError(f"Invalid Protocol Type: {_type}")
    return info[_type]


def get_protocol(uin: int, cache: bool = True) -> ApkInfo:
    protocol_file = Storage.get_account_cache_dir(uin) / "protocol"

    if protocol_file.exists():
        type_ = protocol_file.read_text()
    else:
        type_ = "IPAD"
        protocol_file.write_text(type_)

    protocol = get_apk_info(type_)
    return protocol
