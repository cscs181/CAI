"""StatSvc Packet Builder

This module is used to build and handle StatSvc packets.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""

from typing import Optional

from jce import JceStruct, JceField, types


class VendorPushInfo(JceStruct):
    """Vendor Push Info Jce Packet.

    Note:
        Source: com.tencent.msf.service.protocol.push.VendorPushInfo
    """
    vendor_type: types.INT64 = JceField(jce_id=0)


class SvcReqRegister(JceStruct):
    """Service Request Register Jce Packet.

    Note:
        Source: com.tencent.msf.service.protocol.push.SvcReqRegister
    """
    uin: types.INT64 = JceField(jce_id=0)
    """:obj:`~jce.types.INT64`: uin."""
    bid: types.INT64 = JceField(jce_id=1)
    """:obj:`~jce.types.INT64`: login bid.

    login: 1 | 2 | 4 = 7, logout: 0.
    """
    conn_type: types.BYTE = JceField(0, jce_id=2)
    """:obj:`~jce.types.BYTE`: always 0."""
    other: types.STRING = JceField("", jce_id=3)
    """:obj:`~jce.types.STRING`: unknown."""
    status: types.INT32 = JceField(jce_id=4)
    """:obj:`~jce.types.INT32`: online status.

    online: 11, offline: 21, away: 31, invisible: 41,
    busy: 50, qme: 60, dnd: 70, receive_offline_msg: 95.
    """
    online_push: types.BOOL = JceField(False, jce_id=5)
    """:obj:`~jce.types.BOOL`: unknown."""
    is_online: types.BOOL = JceField(False, jce_id=6)
    """:obj:`~jce.types.BOOL`: is online."""
    is_show_online: types.BOOL = JceField(False, jce_id=7)
    """:obj:`~jce.types.BOOL`: is show online."""
    kick_pc: types.BOOL = JceField(False, jce_id=8)
    """:obj:`~jce.types.BOOL`: whether to kick pc or not."""
    kick_weak: types.BOOL = JceField(False, jce_id=9)
    """:obj:`~jce.types.BOOL`: kick weak."""
    timestamp: types.INT64 = JceField(0, jce_id=10)
    """:obj:`~jce.types.INT64`: timestamp."""
    ios_version: types.INT64 = JceField(jce_id=11)
    """:obj:`~jce.types.INT64`: android sdk version."""
    nettype: types.BYTE = JceField(jce_id=12)
    """:obj:`~jce.types.BYTE`: nettype.

    wifi: 1, mobile: 0.
    """
    build_version: types.STRING = JceField("", jce_id=13)
    """:obj:`~jce.types.STRING`: build version."""
    reg_type: types.BYTE = JceField(jce_id=14)
    """:obj:`~jce.types.BYTE`: reg push reason.

    appRegister, fillRegProxy, createDefaultRegInfo, setOnlineStatus: 0; else 1.
    """
    dev_param: Optional[types.BYTES] = JceField(None, jce_id=15)
    guid: Optional[types.BYTES] = JceField(None, jce_id=16)
    locale_id: types.INT32 = JceField(jce_id=17)
    slient_push: types.BYTE = JceField(jce_id=18)
    dev_name: types.STRING = JceField("", jce_id=19)
    dev_type: types.STRING = JceField("", jce_id=20)
    os_version: types.STRING = JceField("", jce_id=21)
    open_push: types.BOOL = JceField(True, jce_id=22)
    large_seq: types.INT64 = JceField(jce_id=23)
    last_watch_start_time: types.INT64 = JceField(jce_id=24)
    bind_uin: types.LIST[types.JceType] = JceField(types.LIST(), jce_id=25)
    old_sso_ip: types.INT64 = JceField(jce_id=26)
    new_sso_ip: types.INT64 = JceField(jce_id=27)
    channel_num: types.STRING = JceField("", jce_id=28)
    cp_id: types.INT64 = JceField(jce_id=29)
    vendor_name: Optional[types.STRING] = JceField(None, jce_id=30)
    vendor_os_name: Optional[types.STRING] = JceField(None, jce_id=31)
    ios_idfa: Optional[types.STRING] = JceField(None, jce_id=32)
    b769: Optional[types.BYTES] = JceField(None, jce_id=33)
    is_set_status: types.BOOL = JceField(jce_id=34)
    """:obj:`~jce.types.BOOL`: is set status.

    reg push reason:
        setOnlineStatus: True, else: False.
    """
    server_buf: Optional[types.BYTES] = JceField(None, jce_id=35)
    set_mute: types.BOOL = JceField(jce_id=36)
    ext_online_status: types.INT64 = JceField(jce_id=38)
    battery_status: types.INT32 = JceField(jce_id=39)
    vendor_push_info: Optional[VendorPushInfo] = JceField(None, jce_id=42)
