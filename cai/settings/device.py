import uuid
import random
import secrets
from hashlib import md5
from typing import Optional
from dataclasses import dataclass


@dataclass(init=True, eq=False)
class Version:
    __slots__ = ("incremental", "release", "codename", "sdk")

    incremental: str
    release: str = "10"
    codename: str = "REL"
    sdk: int = 29


@dataclass(init=True, eq=False)
class DeviceInfo:
    product: str
    device: str
    board: str
    brand: str
    model: str
    bootloader: str
    boot_id: str
    proc_version: str
    baseband: str
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

    @property
    def display(self) -> str:
        return self.android_id

    @property
    def fingerprint(self) -> str:
        return f"{self.brand}/{self.product}/{self.device}:10/{self.android_id}/{self.version.incremental}:user/release-keys"

    @property
    def wifi_bssid(self) -> str:
        return self.mac_address

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


def new_device(product: Optional[str] = None,
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
               version: Optional[Version] = None) -> DeviceInfo:
    return DeviceInfo(product=product or "iarim",
                      device=device or "sagit",
                      board=board or "eomam",
                      brand=brand or "Xiaomi",
                      model=model or "MI 10",
                      bootloader=bootloader or "U-boot",
                      boot_id=boot_id or new_boot_id(),
                      proc_version=proc_version or new_proc_version(),
                      baseband=baseband or "",
                      mac_address=mac_address or new_mac_address(),
                      ip_address=ip_address or new_ip_address(),
                      wifi_ssid=wifi_ssid or "<unknown ssid>",
                      imei=imei or new_imei(),
                      android_id=android_id or new_android_id(),
                      version=version or new_version())
