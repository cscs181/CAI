"""SSO Server SDK

This module is used to get server list and choose the best one.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

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
    """Fake socket object.

    This class is used to wrap raw response bytes
    and pass them to :class:`http.client.HTTPResponse`.

    Args:
        response (:obj:`bytes`): HTTP raw response from server.
    """

    def __init__(self, response: bytes):
        self._file = BytesIO(response)

    def makefile(self, *args, **kwargs):
        return self._file


class SsoServerRequest(JceStruct):
    """Sso Server List Request.

    Note:
        Source: com.tencent.msf.service.protocol.serverconfig.d
    """
    uin: types.INT64 = JceField(0, jce_id=1)  # uin or 0
    """:obj:`~jce.types.INT64`: User QQ or 0, renamed from a."""
    timeout: types.INT64 = JceField(0, jce_id=2)
    """:obj:`~jce.types.INT64`: may be timeout (s), default is 60, renamed from b."""
    c: types.BYTE = JceField(bytes([1]), jce_id=3)
    """:obj:`~jce.types.BYTE`: always 1."""
    imsi: types.STRING = JceField("46000", jce_id=4)
    """:obj:`~jce.types.STRING`: imsi string, renamed from d.

    ``null``->``""`` or ``imsi.substring(0, 5)``.
    """
    is_wifi: types.INT32 = JceField(100, jce_id=5)
    """:obj:`~jce.types.INT32`: is_wifi, renamed from e.

    NetConnInfoCenter.isWifiConn: true->100, false->1.
    """
    app_id: types.INT64 = JceField(jce_id=6)
    """:obj:`~jce.types.INT64`: app_id, renamed from f.

    same to :attr:`cai.settings.protocol.ApkInfo.app_id`.
    """
    imei: types.STRING = JceField(jce_id=7)
    """:obj:`~jce.types.STRING`: imei, renamed from g.

    same to :attr:`cai.settings.device.DeviceInfo.imei`.
    """
    cell_id: types.INT64 = JceField(0, jce_id=8)
    """:obj:`~jce.types.INT64`: cell_id, renamed from h.

    cell location get from ``CdmaCellLocation.getBaseStationId``.
    """
    i: types.INT64 = JceField(0, jce_id=9)
    """:obj:`~jce.types.INT64`: unknown."""
    j: types.INT64 = JceField(0, jce_id=10)
    """:obj:`~jce.types.INT64`: unknown."""
    k: types.BYTE = JceField(bytes(1), jce_id=11)
    """:obj:`~jce.types.BYTE`: unknown boolean, true->1, false->0."""
    l: types.BYTE = JceField(bytes(1), jce_id=12)
    """:obj:`~jce.types.BYTE`: active net ip family.

    get from ``NetConnInfoCenter.getActiveNetIpFamily``.
    """
    m: types.INT64 = JceField(0, jce_id=13)
    """:obj:`~jce.types.INT64`: unknown."""


class SsoServer(JceStruct):
    """Sso Server Info.

    Note:
        Source: com.tencent.msf.service.protocol.serverconfig.i
    """
    host: types.STRING = JceField(jce_id=1)
    """:obj:`~jce.types.STRING`: server host, renamed from a."""
    port: types.INT32 = JceField(jce_id=2)
    """:obj:`~jce.types.INT32`: server port, renamed from b."""
    # c: types.BYTE = JceField(jce_id=3)
    # d: types.BYTE = JceField(jce_id=4)
    protocol: types.BYTE = JceField(jce_id=5)
    """:obj:`~jce.types.BYTE`: protocol, renamed from e.

    0, 1: socket; 2, 3: http.
    """
    # f: types.INT32 = JceField(jce_id=6)
    # g: types.BYTE = JceField(jce_id=7)
    city: types.STRING = JceField(jce_id=8)
    """:obj:`~jce.types.STRING`: city, renamed from h."""
    country: types.STRING = JceField(jce_id=9)
    """:obj:`~jce.types.STRING`: country, renamed from i."""


class SsoServerResponse(JceStruct):
    """Sso Server List Response.

    Note:
        Source: com.tencent.msf.service.protocol.serverconfig.e
    """
    # a: types.INT32 = JceField(0, jce_id=1)
    socket_v4_mobile: types.LIST[SsoServer] = JceField(jce_id=2)
    """:obj:`~jce.types.LIST` of :obj:`.SsoServer`:
    socket ipv4 mobile server, renamed from b.
    """
    socket_v4_wifi: types.LIST[SsoServer] = JceField(jce_id=3)
    """:obj:`~jce.types.LIST` of :obj:`.SsoServer`:
    socket ipv4 wifi server, renamed from c.
    """
    # d: types.INT32 = JceField(0, jce_id=4)
    # e: types.INT32 = JceField(86400, jce_id=5)
    # f: types.BYTE = JceField(bytes(1), jce_id=6)
    # g: types.BYTE = JceField(bytes(1), jce_id=7)
    # h: types.INT32 = JceField(1, jce_id=8)
    # i: types.INT32 = JceField(5, jce_id=9)
    # j: types.INT64 = JceField(0, jce_id=10)
    # k: types.INT32 = JceField(0, jce_id=11)
    http_v4_mobile: types.LIST[SsoServer] = JceField(jce_id=12)
    """:obj:`~jce.types.LIST` of :obj:`.SsoServer`:
    http ipv4 mobile server, renamed from l.
    """
    http_v4_wifi: types.LIST[SsoServer] = JceField(jce_id=13)
    """:obj:`~jce.types.LIST` of :obj:`.SsoServer`:
    http ipv4 wifi server, renamed from m.
    """
    speed_info: types.BYTES = JceField(jce_id=14)
    """:obj:`~jce.types.BYTES`: vCesuInfo, renamed from n.

    bytes from :class:`~cai.utils.jce.RequestPacketVersion3`(QualityTest)
    """
    socket_v6: types.LIST[SsoServer] = JceField(jce_id=15)
    """:obj:`~jce.types.LIST` of :obj:`.SsoServer`:
    socket ipv6 server, renamed from o.

    used when (wifi and :attr:`~.SsoServerResponse.nettype` & 1 == 1)
    or (mobile and :attr:`~.SsoServerResponse.nettype` & 2 == 2)
    """
    http_v6: types.LIST[SsoServer] = JceField(jce_id=16)
    """:obj:`~jce.types.LIST` of :obj:`.SsoServer`:
    http ipv6 server, renamed from p.

    used when (wifi and :attr:`~.SsoServerResponse.nettype` & 1 == 1)
    or (mobile and :attr:`~.SsoServerResponse.nettype` & 2 == 2)
    """
    udp_v6: types.LIST[SsoServer] = JceField(jce_id=17)
    """:obj:`~jce.types.LIST` of :obj:`.SsoServer`:
    quic ipv6 server, renamed from q.

    used when (wifi and :attr:`~.SsoServerResponse.nettype` & 1 == 1)
    or (mobile and :attr:`~.SsoServerResponse.nettype` & 2 == 2)
    """
    nettype: types.BYTE = JceField(bytes(1), jce_id=18)
    """:obj:`~jce.types.BYTE`: nettype, renamed from r."""
    delay_threshold: types.INT32 = JceField(0, jce_id=19)
    """:obj:`~jce.types.INT32`: delay threshold, renamed from s."""
    policy_id: types.STRING = JceField("", jce_id=20)
    """:obj:`~jce.types.STRING`: policy id, renamed from t."""


async def get_sso_list() -> SsoServerResponse:
    """Do sso server list request and return the response.

    Note:
        Source: com.tencent.mobileqq.msf.core.a.f.run

    Returns:
        SsoServerResponse: Sso server list response

    Raises:
        SsoServerException: Get sso server list failed.
    """
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
    """Test given servers' quality by tcp latency.

    Args:
        servers (Iterable[:obj:`.SsoServer`]): Server list to test.
        threshold (float, optional): Latency more than threshold will not be returned.
            Defaults to 500.0.

    Returns:
        List[Tuple[:obj:`.SsoServer`, float]]: List of server and latency in tuple.
    """
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
    """Get the best sso server

    Args:
        cache (bool, optional): Using cache or not. Defaults to True.

    Returns:
        :obj:`.SsoServer`: The best server with smallest latency.
    """
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
