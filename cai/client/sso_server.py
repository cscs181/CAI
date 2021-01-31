from rtea import qqtea_encrypt
from jce import JceStruct, JceField, types

from cai.connection import connect
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol
from cai.utils.jce import RequestPacketVersion3


# com/tencent/msf/service/protocol/serverconfig/C32504d.java
# renamed from: com.tencent.msf.service.protocol.serverconfig.d
class SsoServerRequest(JceStruct):
    uin: types.INT64 = JceField(0, jce_id=1)  # uin or 0
    timeout: types.INT64 = JceField(
        60, jce_id=2
    )  # may be timeout (s), default is 60

    f172842c: types.BYTE = JceField(bytes([1]), jce_id=3)  # always 1
    imsi: types.STRING = JceField(
        "46000", jce_id=4
    )  # imsi: null->'' or imsi.substring(0, 5)
    is_wifi: types.INT32 = JceField(
        100, jce_id=5
    )  # NetConnInfoCenter.isWifiConn: true->100, false->1
    app_id: types.INT64 = JceField(
        jce_id=6
    )  # cai.settings.protocol.ApkInfo.app_id
    imei: types.STRING = JceField(jce_id=7)  # imei
    cell_id: types.INT64 = JceField(
        0, jce_id=8
    )  # CdmaCellLocation.getBaseStationId
    f172848i: types.INT64 = JceField(0, jce_id=9)
    f172849j: types.INT64 = JceField(0, jce_id=10)
    f172850k: types.BYTE = JceField(
        bytes(1), jce_id=11
    )  # Unknown bool(false): true->1, false->0
    f172851l: types.BYTE = JceField(
        bytes(1), jce_id=12
    )  # NetConnInfoCenter.getActiveNetIpFamily
    f172852m: types.INT64 = JceField(0, jce_id=13)


# com/tencent/mobileqq/msf/core/p205a/C25979f.java
async def get_sso_address():
    device = get_device()
    protocol = get_protocol()
    key = bytes(
        [
            0xF0, 0x44, 0x1F, 0x5F, 0xF4, 0x2D, 0xA5, 0x8F, 0xDC, 0xF7, 0x94,
            0x9A, 0xBA, 0x62, 0xD4, 0x11
        ]
    )
    payload = SsoServerRequest.to_bytes(
        0, SsoServerRequest(app_id=protocol.app_id, imei=device.imei)
    )
    packet = RequestPacketVersion3(
        req_id=0,
        servant_name="HttpServerListReq",
        func_name="HttpServerListReq",
        data=types.MAP(
            {types.STRING("HttpServerListReq"): types.BYTES(payload)}
        )
    ).encode(with_length=True)
    buffer = qqtea_encrypt(packet, key)
    async with connect("configsvr.msf.3g.qq.com", 443, ssl=True) as conn:
        query = (
            b"POST /configsvr/serverlist.jsp HTTP/1.1\r\n"
            b"User-Agent: QQ/8.2.0.1296 CFNetwork/1126\r\n"
            b"Net-Type: Wifi\r\n"
            b"Content-Length: " + str(len(buffer)).encode() + b"\r\n"
            b"\r\n" + buffer
        )
        await conn._write_bytes(query)
        response = await conn._read_all()
        print(response)
