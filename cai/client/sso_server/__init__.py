"""SSO Server SDK.

This module is used to get server list and choose the best one.

:Copyright: Copyright (C) 2021-2021  cscs181:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import asyncio
import http.client
from io import BytesIO
from typing import List, Tuple, Union, Iterable, Optional, Container

from jce import types
from rtea import qqtea_decrypt, qqtea_encrypt

from cai.connection import connect
from cai.settings.device import get_device
from cai.exceptions import SsoServerException
from cai.settings.protocol import get_protocol
from cai.utils.jce import RequestPacketVersion3
from cai.connection.utils import tcp_latency_test

from .jce import SsoServer, SsoServerRequest, SsoServerResponse

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
            0xF0,
            0x44,
            0x1F,
            0x5F,
            0xF4,
            0x2D,
            0xA5,
            0x8F,
            0xDC,
            0xF7,
            0x94,
            0x9A,
            0xBA,
            0x62,
            0xD4,
            0x11,
        ]
    )
    payload = SsoServerRequest.to_bytes(
        0, SsoServerRequest(app_id=protocol.app_id, imei=device.imei)
    )
    req_packet = RequestPacketVersion3(
        servant_name="HttpServerListReq",
        func_name="HttpServerListReq",
        data=types.MAP(
            {types.STRING("HttpServerListReq"): types.BYTES(payload)}
        ),
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
        conn.write(query)
        conn.write_eof()
        resp_bytes = await conn.read_all()
        response = http.client.HTTPResponse(
            _FakeSocket(resp_bytes)  # type: ignore
        )
        response.begin()

    if response.status != 200:
        raise SsoServerException(
            f"Get sso server list failed with response code {response.status}"
        )
    data: bytes = qqtea_decrypt(response.read(), key)
    resp_packet = RequestPacketVersion3.decode(data[4:])
    server_info = SsoServerResponse.decode(
        resp_packet.data["HttpServerListRes"][1:-1]  # type: ignore
    )
    return server_info


async def quality_test(
    servers: Iterable[SsoServer], threshold: float = 500.0
) -> List[Tuple[SsoServer, float]]:
    """Test given servers' quality by tcp latency.

    Args:
        servers (Iterable[:obj:`.SsoServer`]): Server list to test.
        threshold (float, optional): Latency more than threshold will not be returned.
            Defaults to 500.0.

    Returns:
        List[Tuple[:obj:`.SsoServer`, float]]: List of server and latency in tuple.
    """
    servers_ = list(servers)
    tasks = [tcp_latency_test(server.host, server.port) for server in servers_]
    result: List[Union[float, Exception]] = await asyncio.gather(
        *tasks, return_exceptions=True
    )
    success_servers = [
        (server, latency)
        for server, latency in zip(servers_, result)
        if isinstance(latency, float) and latency < threshold
    ]
    return success_servers


async def get_sso_server(
    cache: bool = True,
    cache_server_list: bool = True,
    exclude: Optional[Container[str]] = None,
) -> SsoServer:
    """Get the best sso server

    Args:
        cache (bool, optional): Using cache server or not. Defaults to True.
        cache_server_list (bool, optional): Using cache server list or not. Defaults to True.
        exclude (List[str], optional): List of servers' ip want to be excluded

    Returns:
        :obj:`.SsoServer`: The best server with smallest latency.
    """
    global _cached_server
    if cache and _cached_server:
        return _cached_server

    if cache_server_list and _cached_servers:
        servers = _cached_servers
    else:
        sso_list = await get_sso_list()
        servers = [*sso_list.socket_v4_mobile, *sso_list.socket_v4_wifi]
        _cached_servers.clear()
        _cached_servers.extend(servers)

    exclude_server = exclude or []
    success_servers = await quality_test(
        server for server in servers if server.host not in exclude_server
    )
    success_servers.sort(key=lambda x: x[1])
    _cached_server = success_servers[0][0]
    return _cached_server
