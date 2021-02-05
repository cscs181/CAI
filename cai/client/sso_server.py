"""SSO Server SDK

This module is used to get server list and choose the best one.

Copyright (C) 2021-2021  yanyongyu

License AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import asyncio
import http.client
from io import BytesIO
from typing import List, Union, Tuple, Iterable, Optional

from jce import JceStruct, JceField, types
from rtea import qqtea_encrypt, qqtea_decrypt

from cai.connection import connect
from cai.settings.device import get_device
from cai.exceptions import SsoServerException
from cai.settings.protocol import get_protocol
from cai.utils.jce import RequestPacketVersion3
from cai.connection.utils import tcp_latency_test

_cached_server: Optional["SsoServer"] = None
_cached_servers: List["SsoServer"] = []


class _FakeSocket:

    def __init__(self, response: bytes):
        self._file = BytesIO(response)

    def makefile(self, *args, **kwargs):
        return self._file


# renamed from: com.tencent.msf.service.protocol.serverconfig.d
class SsoServerRequest(JceStruct):
    uin: types.INT64 = JceField(0, jce_id=1)  # uin or 0
    timeout: types.INT64 = JceField(
        0, jce_id=2
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


# renamed from: com.tencent.msf.service.protocol.serverconfig.i
class SsoServer(JceStruct):
    host: types.STRING = JceField(jce_id=1)
    port: types.INT32 = JceField(jce_id=2)
    # f172901c: types.BYTE = JceField(jce_id=3)
    # f172902d: types.BYTE = JceField(jce_id=4)
    protocol: types.BYTE = JceField(jce_id=5)  # 0,1: socket; 2,3: http
    # f172904f: types.INT32 = JceField(jce_id=6)
    # f172905g: types.BYTE = JceField(jce_id=7)
    city: types.STRING = JceField(jce_id=8)
    country: types.STRING = JceField(jce_id=9)


# renamed from: com.tencent.msf.service.protocol.serverconfig.e
class SsoServerResponse(JceStruct):
    # f172861a: types.INT32 = JceField(0, jce_id=1)
    socket_v4_mobile: types.LIST[SsoServer] = JceField(
        jce_id=2
    )  # socket, ipv4, mobile
    socket_v4_wifi: types.LIST[SsoServer] = JceField(
        jce_id=3
    )  # socket, ipv4, wifi
    # f172864d: types.INT32 = JceField(0, jce_id=4)
    # f172865e: types.INT32 = JceField(86400, jce_id=5)
    # f172866f: types.BYTE = JceField(bytes(1), jce_id=6)
    # f172867g: types.BYTE = JceField(bytes(1), jce_id=7)
    # f172868h: types.INT32 = JceField(1, jce_id=8)
    # f172869i: types.INT32 = JceField(5, jce_id=9)
    # f172870j: types.INT64 = JceField(0, jce_id=10)
    # f172871k: types.INT32 = JceField(0, jce_id=11)
    http_v4_mobile: types.LIST[SsoServer] = JceField(
        jce_id=12
    )  # http, ipv4, mobile
    http_v4_wifi: types.LIST[SsoServer] = JceField(
        jce_id=13
    )  # http, ipv4, wifi
    speed_info: types.BYTES = JceField(
        jce_id=14
    )  # vCesuInfo, PacketVersion3(QualityTest)
    socket_v6: types.LIST[SsoServer] = JceField(
        jce_id=15
    )  # socket, ipv6, (wifi and nettype & 1 == 1) | (mobile and nettype & 2 == 2)
    http_v6: types.LIST[SsoServer] = JceField(
        jce_id=16
    )  # http, ipv6, (wifi and nettype & 1 == 1) | (mobile and nettype & 2 == 2)
    udp_v6: types.LIST[SsoServer] = JceField(
        jce_id=17
    )  # quic, ipv6, (wifi and nettype & 1 == 1) | (mobile and nettype & 2 == 2)
    nettype: types.BYTE = JceField(bytes(1), jce_id=18)
    delay_threshold: types.INT32 = JceField(0, jce_id=19)
    policy_id: types.STRING = JceField("", jce_id=20)


# com/tencent/mobileqq/msf/core/p205a/C25979f.java
async def get_sso_list() -> SsoServerResponse:
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
    req_packet = RequestPacketVersion3(
        req_id=0,
        servant_name="HttpServerListReq",
        func_name="HttpServerListReq",
        data=types.MAP(
            {types.STRING("HttpServerListReq"): types.BYTES(payload)}
        )
    ).encode(with_length=True)
    buffer: bytes = qqtea_encrypt(req_packet, key)
    async with connect("configsvr.msf.3g.qq.com", 443, ssl=True) as conn:
        query = (
            b"POST /configsvr/serverlist.jsp HTTP/1.1\r\n"
            b"Host: configsvr.msf.3g.qq.com\r\n"
            b"User-Agent: QQ/8.4.1.2703 CFNetwork/1126\r\n"
            b"Net-Type: Wifi\r\n"
            b"Accept: */*\r\n"
            b"Connection: close\r\n"
            b"Content-Type: application/octet-stream\r\n"
            b"Content-Length: " + str(len(buffer)).encode() + b"\r\n"
            b"\r\n" + buffer
        )
        conn._write_bytes(query)
        conn._write_eof()
        resp_bytes = await conn._read_all()
        response = http.client.HTTPResponse(
            _FakeSocket(resp_bytes)  # type: ignore
        )
        response.begin()

    if response.status != 200:
        raise SsoServerException(
            f"Get sso server list failed with response code {response.status}"
        )
    data: bytes = qqtea_decrypt(response.read(), key)
    resp_packet = RequestPacketVersion3.decode(data)
    server_info = SsoServerResponse.decode(
        resp_packet.data["HttpServerListRes"][1:-1]
    )
    return server_info


async def quality_test(
    servers: Iterable[SsoServer],
    threshold: float = 500.
) -> List[Tuple[SsoServer, float]]:
    tasks = [tcp_latency_test(server.host, server.port) for server in servers]
    result: List[Union[float, Exception]
                ] = await asyncio.gather(*tasks, return_exceptions=True)
    success_servers = [
        (server, latency)
        for server, latency in zip(servers, result)
        if isinstance(latency, float) and latency < threshold
    ]
    return success_servers


async def get_sso_server(cache: bool = True) -> SsoServer:
    global _cached_server
    if cache and _cached_server:
        return _cached_server
    if cache and _cached_servers:
        servers = _cached_servers
    else:
        sso_list = await get_sso_list()
        servers = [*sso_list.socket_v4_mobile, *sso_list.socket_v4_wifi]
        _cached_servers.clear()
        _cached_servers.extend(servers)
    success_servers = await quality_test(servers)
    success_servers.sort(key=lambda x: x[1])
    _cached_server = success_servers[0][0]
    return _cached_server
