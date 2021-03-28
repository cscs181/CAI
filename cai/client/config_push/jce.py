"""ConfigPushSvc Packet Builder.

This module is used to build and handle ConfigPushSvc packets.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""

from typing import Optional

from jce import JceStruct, JceField, types

from cai.client.sso_server import SsoServer


class PushReq(JceStruct):
    """
    Note:
        Source: ConfigPush.PushReq
    """
    type: types.INT32 = JceField(jce_id=1)
    jcebuf: types.BYTES = JceField(jce_id=2)
    large_seq: types.INT64 = JceField(jce_id=3)


class FileServerInfo(JceStruct):
    """
    Note:
        Source: ConfigPush.FileStorageServerListInfo
    """
    ip: types.STRING = JceField(jce_id=1)
    port: types.INT32 = JceField(jce_id=2)


class BigDataIpInfo(JceStruct):
    """
    Note:
        Source: ConfigPush.BigDataIpInfo
    """
    type: types.INT64 = JceField(jce_id=0)
    ip: types.STRING = JceField(jce_id=1)
    port: types.INT64 = JceField(jce_id=2)


class NetSegConf(JceStruct):
    """
    Note:
        Source: ConfigPush.NetSegConf
    """
    net_type: Optional[types.INT64] = JceField(None, jce_id=0)
    segsize: Optional[types.INT64] = JceField(None, jce_id=1)
    segnum: Optional[types.INT64] = JceField(None, jce_id=2)
    cur_conn_num: Optional[types.INT64] = JceField(None, jce_id=3)


class BigDataIpList(JceStruct):
    """
    Note:
        Source: ConfigPush.BigDataIpList
    """
    service_type: types.INT64 = JceField(jce_id=0)
    ip_list: types.LIST[BigDataIpInfo] = JceField(jce_id=1)
    net_seg_confs: Optional[types.LIST[NetSegConf]] = JceField(None, jce_id=2)
    fragment_size: Optional[types.INT64] = JceField(None, jce_id=3)


class BigDataChannel(JceStruct):
    """
    Note:
        Source: ConfigPush.BigDataChannel
    """
    bigdata_iplists: types.LIST[BigDataIpList] = JceField(jce_id=0)
    bigdata_sig_session: Optional[types.BYTES] = JceField(None, jce_id=1)
    bigdata_key_session: Optional[types.BYTES] = JceField(None, jce_id=2)
    sig_uin: Optional[types.INT64] = JceField(None, jce_id=3)
    connect_flag: Optional[types.INT32] = JceField(None, jce_id=4)
    bigdata_pb_buf: Optional[types.BYTES] = JceField(None, jce_id=5)


class FmtIpInfo(JceStruct):
    """
    Note:
        Source: ConfigPush.FmtIpInfo
    """
    gate_ip: types.STRING = JceField(jce_id=0)
    gate_ip_order: types.INT64 = JceField(jce_id=1)


class DomainIpInfo(JceStruct):
    """
    Note:
        Source: ConfigPush.DomainIpInfo
    """
    ip: types.INT32 = JceField(jce_id=1)
    port: types.INT32 = JceField(jce_id=2)


class DomainIpList(JceStruct):
    """
    Note:
        Source: ConfigPush.DomainIpList
    """
    domain_type: types.INT32 = JceField(jce_id=0)
    ip_list: types.LIST[DomainIpInfo] = JceField(jce_id=1)


class DomainIpChannel(JceStruct):
    """
    Note:
        Source: ConfigPush.DomainIpChannel
    """
    domain_iplists: types.LIST[DomainIpList] = JceField(jce_id=0)


class FileServerPushList(JceStruct):
    """
    Note:
        Source: ConfigPush.FileStoragePushFSSvcList
    """
    upload_list: types.LIST[FileServerInfo] = JceField(jce_id=0)
    pic_download_list: types.LIST[FileServerInfo] = JceField(jce_id=1)
    g_pic_download_list: Optional[types.LIST[FileServerInfo]
                                 ] = JceField(None, jce_id=2)
    qzone_proxy_service_list: Optional[types.LIST[FileServerInfo]
                                      ] = JceField(None, jce_id=3)
    url_encode_service_list: Optional[types.LIST[FileServerInfo]
                                     ] = JceField(None, jce_id=4)
    big_data_channel: Optional[BigDataChannel] = JceField(None, jce_id=5)
    vip_emotion_list: Optional[types.LIST[FileServerInfo]
                              ] = JceField(None, jce_id=6)
    c2c_pic_down_list: Optional[types.LIST[FileServerInfo]
                               ] = JceField(None, jce_id=7)
    fmt_ip_info: Optional[FmtIpInfo] = JceField(None, jce_id=8)
    domain_ip_channel: Optional[DomainIpChannel] = JceField(None, jce_id=9)
    ptt_list: Optional[types.BYTES] = JceField(None, jce_id=10)


class SsoServerPushList(JceStruct):
    """
    Note:
        Source: com.tencent.msf.service.protocol.serverconfig.C32524j
    """
    socket_v4_mobile: types.LIST[SsoServer] = JceField(jce_id=1)
    """:obj:`~jce.types.LIST` of :obj:`~cai.client.sso_server.jce.SsoServer`:
    socket ipv4 mobile server, renamed from a.
    """
    socket_v4_wifi: types.LIST[SsoServer] = JceField(jce_id=3)
    """:obj:`~jce.types.LIST` of :obj:`~cai.client.sso_server.jce.SsoServer`:
    socket ipv4 wifi server, renamed from b.
    """
    # c: types.INT32 = JceField(jce_id=4)
    # d: types.BYTE = JceField(jce_id=5)
    # e: types.BYTE = JceField(jce_id=6)
    # f: types.INT32 = JceField(jce_id=7)
    http_v4_mobile: types.LIST[SsoServer] = JceField(jce_id=8)
    """:obj:`~jce.types.LIST` of :obj:`~cai.client.sso_server.jce.SsoServer`:
    http ipv4 mobile server, renamed from g.
    """
    http_v4_wifi: types.LIST[SsoServer] = JceField(jce_id=9)
    """:obj:`~jce.types.LIST` of :obj:`~cai.client.sso_server.jce.SsoServer`:
    http ipv4 wifi server, renamed from h.
    """
    udp_v4: types.LIST[SsoServer] = JceField(jce_id=10)
    """:obj:`~jce.types.LIST` of :obj:`~cai.client.sso_server.jce.SsoServer`:
    quic ipv4 server, renamed from i.
    """
    socket_v6: types.LIST[SsoServer] = JceField(jce_id=11)
    """:obj:`~jce.types.LIST` of :obj:`~cai.client.sso_server.jce.SsoServer`:
    socket ipv6 server, renamed from j.

    used when (wifi and :attr:`~.SsoServerPushList.nettype` & 1 == 1)
    or (mobile and :attr:`~.SsoServerPushList.nettype` & 2 == 2)
    """
    http_v6: types.LIST[SsoServer] = JceField(jce_id=12)
    """:obj:`~jce.types.LIST` of :obj:`~cai.client.sso_server.jce.SsoServer`:
    http ipv6 server, renamed from k.

    used when (wifi and :attr:`~.SsoServerPushList.nettype` & 1 == 1)
    or (mobile and :attr:`~.SsoServerPushList.nettype` & 2 == 2)
    """
    udp_v6: types.LIST[SsoServer] = JceField(jce_id=13)
    """:obj:`~jce.types.LIST` of :obj:`~cai.client.sso_server.jce.SsoServer`:
    quic ipv6 server, renamed from l.

    used when (wifi and :attr:`~.SsoServerPushList.nettype` & 1 == 1)
    or (mobile and :attr:`~.SsoServerPushList.nettype` & 2 == 2)
    """
    nettype: types.BYTE = JceField(bytes(1), jce_id=14)
    """:obj:`~jce.types.BYTE`: nettype, renamed from m."""
    delay_threshold: types.INT32 = JceField(0, jce_id=15)
    """:obj:`~jce.types.INT32`: delay threshold, renamed from n."""
    policy_id: types.STRING = JceField("", jce_id=16)
    """:obj:`~jce.types.STRING`: policy id, renamed from o."""
