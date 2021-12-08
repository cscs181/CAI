"""SSO Server Packet Builder.

This module is used to build sso server packets.

:Copyright: Copyright (C) 2021-2021  cscs181:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from jce import JceField, JceStruct, types


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

    bytes from :class:`~cai.utils.jce.RequestPacketVersion3` (QualityTest)
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
