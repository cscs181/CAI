import sys
import logging
import unittest
import unittest.mock
from hashlib import md5

from cai.log import logger
import cai.settings.device as device
import cai.settings.protocol as protocol

# clear cache
for module in list(sys.modules.keys()):
    if module.startswith("cai") and not module in [
        "cai.settings.device",
        "cai.settings.protocol",
        "cai.log",
    ]:
        del sys.modules[module]

mock_device = unittest.mock.patch.object(
    device,
    "get_device",
    return_value=device.DeviceInfo(
        product="missi",
        device="venus",
        board="venus",
        brand="Xiaomi",
        model="MI 11",
        vendor_name="MIUI",
        vendor_os_name="MIUI",
        bootloader="unknown",
        boot_id="dc109fd7-f17f-4f43-a266-b68469c19a1f",
        proc_version="Linux version 4.19.71-ab0b8e88 (android-build@github.com)",
        baseband="",
        mac_address="89:C2:A9:C5:FA:E9",
        ip_address="10.0.46.76",
        wifi_ssid="<unknown ssid>",
        imei="862542082770767",
        android_id="BRAND.141613.779",
        version=device.Version(
            incremental="V12.0.19.0.RKBCNXM",
            release="11",
            codename="REL",
            sdk=30,
        ),
        sim="T-Mobile",
        os_type="android",
        apn="wifi",
        _imsi_md5="0f63d5c351fd1d75a29d88cae86d315d",
        _tgtgt_md5="c4e512e6924e4872e552e861a914d49a",
        _guid_md5=None,
    ),
)
mock_protocol = unittest.mock.patch.object(
    protocol,
    "get_protocol",
    return_value=protocol.ApkInfo(
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
    ),
)

with mock_device:
    with mock_protocol:
        from cai.settings.device import get_device
        from cai.client.wtlogin import encode_login_request9


class TestEncodeLoginRequest(unittest.IsolatedAsyncioTestCase):
    def log(self, level: int, message: str, *args, exc_info=False, **kwargs):
        message = "| TestEncodeLoginRequest | " + message
        return logger.log(level, message, *args, exc_info=exc_info, **kwargs)

    def setUp(self):
        self.log(logging.INFO, "Start Testing Encode Login Request...")

    def tearDown(self):
        self.log(logging.INFO, "End Testing Encode Login Request!")

    def test_encode_login_request(self):
        self.log(logging.INFO, "test encode login request")
        # ensure encode has no error
        packet = encode_login_request9(
            10,
            bytes(16),
            bytes([0x02, 0xB0, 0x5B, 0x8B]),
            f"|{get_device().imei}|A8.2.7.27f6ea96".encode(),
            123456,
            md5("123456".encode()).digest(),
        )
        # print(packet.hex())


if __name__ == "__main__":
    unittest.main()
