"""ConfigPushSvc Packet Builder.

This module is used to build and handle ConfigPushSvc packets.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""

from typing import Optional

from jce import JceStruct, JceField, types


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
    domain_iplists: DomainIpList = JceField(jce_id=0)


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
