import uuid
import random
import secrets
from hashlib import md5
from dataclasses import dataclass


@dataclass
class Version:
    incremental: str
    release: str = "10"
    codename: str = "REL"
    sdk: int = 29


@dataclass
class DeviceInfo:
    display: str
    product: str
    device: str
    board: str
    brand: str
    model: str
    bootloader: str
    fingerprint: str
    boot_id: str
    proc_version: str
    baseband: str
    mac_address: str
    ip_address: str
    wifi_bssid: str
    wifi_ssid: str
    imei: str
    android_id: str
    version: Version
    sim: str = "T-Mobile"
    os_type: str = "android"
    apn: str = "wifi"
    _imsi_md5: str = md5(secrets.token_bytes(16)).hexdigest()
    _tgtgt_md5: str = md5(secrets.token_bytes(16)).hexdigest()

    @property
    def imsi(self) -> bytes:
        return bytes.fromhex(self._imsi_md5)

    @property
    def tgtgt(self) -> bytes:
        return bytes.fromhex(self._tgtgt_md5)


def _get_local_mac_address() -> int:
    return uuid.getnode()


def new_mac_address() -> str:
    addr = hex(_get_local_mac_address()).upper()
    return ":".join(addr[x:x + 2] for x in range(2, 14, 2))


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
    return f"Linux version 4.19.71-{hex(random.randint(0x10000000, 0xffffffff))[2:]} (android-build@github.com)"


def new_ip_address() -> str:
    return f"10.0.{random.randint(0,99)}.{random.randint(0,99)}"


def new_incremental() -> str:
    return str(random.randint(1000000, 9999999))


def new_version() -> Version:
    return Version(incremental=new_incremental())


def new_device() -> DeviceInfo:
    android_id = new_android_id()
    mac_address = new_mac_address()
    version = new_version()
    return DeviceInfo(
        display=android_id,
        product="iarim",
        device="sagit",
        board="eomam",
        brand="Xiaomi",
        model="MI 11",
        bootloader="U-boot",
        fingerprint=
        f"Xiaomi/iarim/sagit:10/{android_id}/{version.incremental}:user/release-keys",
        boot_id=new_boot_id(),
        proc_version=new_proc_version(),
        baseband="",
        mac_address=mac_address,
        ip_address=new_ip_address(),
        wifi_bssid=mac_address,
        wifi_ssid="<unknown ssid>",
        imei=new_imei(),
        android_id=android_id,
        version=new_version())
