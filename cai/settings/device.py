"""Application Device Setting

This module is used to get or new the application device setting.
Device settings will be stored in APP_DIR provided by storage manager.
Once the device setting is loaded, it will be cached until application shut down.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import os
import time
import uuid
import random
import secrets
from hashlib import md5
from typing import Optional
from dataclasses import dataclass

from cai.log import logger
from cai.storage import Storage
from cai.utils.dataclass import JsonableDataclass

_device: Optional["DeviceInfo"] = None


@dataclass(init=True, eq=False)
class Version(JsonableDataclass):
    __slots__ = ("incremental", "release", "codename", "sdk")
    __json_fields__ = ("incremental", "release", "codename", "sdk")

    incremental: str
    release: str
    codename: str
    sdk: int


@dataclass(init=True, eq=False)
class DeviceInfo(JsonableDataclass):
    # __slots__ not work with dataclass default value
    # __slots__ = (
    #     "product", "device", "board", "model", "bootloader", "boot_id",
    #     "proc_version", "baseband", "vendor_name", "vendor_os_name",
    #     "mac_address", "ip_address", "wifi_ssid", "imei", "android_id",
    #     "version", "sim", "os_type", "apn", "imsi_md5", "tgtgt", "display",
    #     "fingerprint", "wifi_bssid"
    # )
    __json_fields__ = (
        "product",
        "device",
        "board",
        "brand",
        "model",
        "bootloader",
        "boot_id",
        "proc_version",
        "baseband",
        "vendor_name",
        "vendor_os_name",
        "mac_address",
        "ip_address",
        "wifi_ssid",
        "imei",
        "android_id",
        "version",
        "sim",
        "os_type",
        "apn",
        "_imsi_md5",
    )

    product: str
    device: str
    board: str
    brand: str
    model: str
    bootloader: str
    boot_id: str
    proc_version: str
    baseband: str
    vendor_name: str
    vendor_os_name: str
    mac_address: str
    ip_address: str
    wifi_ssid: str
    imei: str
    android_id: str
    version: Version
    sim: str = "T-Mobile"
    os_type: str = "android"
    apn: str = "wifi"
    _imsi_md5: str = md5(secrets.token_bytes(16)).hexdigest()
    _tgtgt_md5: str = md5(secrets.token_bytes(16)).hexdigest()
    _guid_md5: Optional[bytes] = None

    @property
    def display(self) -> str:
        return self.android_id

    @property
    def fingerprint(self) -> str:
        return (
            f"{self.brand}/{self.product}/{self.device}:"
            f"{self.version.release}/{self.android_id}/"
            f"{self.version.incremental}:user/release-keys"
        )

    @property
    def wifi_bssid(self) -> str:
        return self.mac_address

    @property
    def imsi_md5(self) -> bytes:
        return bytes.fromhex(self._imsi_md5)

    @property
    def tgtgt(self) -> bytes:
        return bytes.fromhex(self._tgtgt_md5)

    @tgtgt.setter
    def tgtgt(self, key: bytes):
        self._tgtgt_md5 = key.hex()

    @property
    def guid(self) -> bytes:
        if not self._guid_md5:
            self._guid_md5 = md5(
                (self.android_id + self.mac_address).encode()
            ).digest()
        return self._guid_md5


def _get_local_mac_address() -> int:
    return uuid.getnode()


def new_mac_address() -> str:
    addr = hex(_get_local_mac_address()).upper()
    return ":".join(addr[x : x + 2] for x in range(2, 14, 2))


def _get_imei_sign(imei: str) -> str:
    sum_ = 0
    for i in range(len(imei)):
        j = int(imei[i])
        if i % 2:
            sum_ += (j * 2) % 10 + j * 2 // 10
        else:
            sum_ += j
    return str((100 - sum_) % 10)


def new_imei() -> str:
    imei = f"86{random.randint(100, 9999):04d}0{random.randint(1000000, 9999999):07d}"
    return imei + _get_imei_sign(imei)


def new_android_id() -> str:
    return f"BRAND.{random.randint(1, 999999):06d}.{random.randint(1, 999):03d}"


def new_boot_id() -> str:
    return str(uuid.uuid4())


def new_proc_version() -> str:
    return f"Linux version 4.19.71-{random.randint(0x10000000, 0xffffffff):x} (android-build@github.com)"


def new_ip_address() -> str:
    return f"10.0.{random.randint(0,99)}.{random.randint(0,99)}"


def new_version(
    incremental: Optional[str] = None,
    release: Optional[str] = None,
    codename: Optional[str] = None,
    sdk: Optional[int] = None,
) -> Version:
    return Version(
        incremental=incremental or "V12.0.19.0.RKBCNXM",
        release=release or "11",
        codename=codename or "REL",
        sdk=sdk or 30,
    )


def new_device(
    product: Optional[str] = None,
    device: Optional[str] = None,
    board: Optional[str] = None,
    brand: Optional[str] = None,
    model: Optional[str] = None,
    bootloader: Optional[str] = None,
    boot_id: Optional[str] = None,
    proc_version: Optional[str] = None,
    baseband: Optional[str] = None,
    mac_address: Optional[str] = None,
    ip_address: Optional[str] = None,
    wifi_ssid: Optional[str] = None,
    imei: Optional[str] = None,
    android_id: Optional[str] = None,
    version: Optional[Version] = None,
) -> DeviceInfo:
    return DeviceInfo(
        product=product or "missi",
        device=device or "venus",
        board=board or "venus",
        brand=brand or "Xiaomi",
        model=model or "MI 11",
        bootloader=bootloader or "unknown",
        boot_id=boot_id or new_boot_id(),
        proc_version=proc_version or new_proc_version(),
        baseband=baseband or "",
        vendor_name="MIUI",
        vendor_os_name="MIUI",
        mac_address=mac_address or new_mac_address(),
        ip_address=ip_address or new_ip_address(),
        wifi_ssid=wifi_ssid or "<unknown ssid>",
        imei=imei or new_imei(),
        android_id=android_id or new_android_id(),
        version=version or new_version(),
    )


def get_device(cache: bool = True) -> DeviceInfo:
    global _device
    if cache and _device:
        return _device

    device: DeviceInfo
    if not os.path.exists(Storage.device_file):
        device = new_device()
        with open(Storage.device_file, "w") as f:
            device.to_file(f)
    else:
        with open(Storage.device_file, "r+") as f:
            try:
                device = DeviceInfo.from_file(f)
            except Exception as e:
                backup_file = f"{Storage.device_file}.{int(time.time())}.bak"
                logger.error(
                    "Error when loading device info from config file:\n\n"
                    + repr(e)
                    + f"\n\nRegenerating device info in `{Storage.device_file}`! "
                    + f"The original device info has been backed up in `{backup_file}`."
                )
                f.seek(0)
                with open(backup_file, "w") as fb:
                    fb.write(f.read())
                device = new_device()
                f.seek(0)
                f.truncate(0)
                device.to_file(f)

    _device = device
    return _device
