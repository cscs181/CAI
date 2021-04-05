"""StatSvc Packet Builder.

This module is used to build and handle StatSvc packets.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional

from jce import JceStruct, JceField, types


class VendorPushInfo(JceStruct):
    """Vendor Push Info Jce Packet.

    Note:
        Source: com.tencent.msf.service.protocol.push.VendorPushInfo
    """
    vendor_type: types.INT64 = JceField(0, jce_id=0)
    """:obj:`~jce.types.INT64`: third push type."""


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
    conn_type: types.BYTE = JceField(bytes(1), jce_id=2)
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
    """:obj:`~jce.types.BYTES`: unknown."""
    guid: Optional[types.BYTES] = JceField(None, jce_id=16)
    """:obj:`~jce.types.BYTES`: guid."""
    locale_id: types.INT32 = JceField(2052, jce_id=17)
    """:obj:`~jce.types.INT32`: 2052 by default."""
    slient_push: types.BYTE = JceField(bytes(1), jce_id=18)
    """:obj:`~jce.types.BYTE`: unknown."""
    dev_name: types.STRING = JceField("", jce_id=19)
    """:obj:`~jce.types.STRING`: device model."""
    dev_type: types.STRING = JceField("", jce_id=20)
    """:obj:`~jce.types.STRING`: device model."""
    os_version: types.STRING = JceField("", jce_id=21)
    """:obj:`~jce.types.STRING`: build version release."""
    open_push: types.BOOL = JceField(True, jce_id=22)
    """:obj:`~jce.types.BOOL`: open push."""
    large_seq: types.INT64 = JceField(jce_id=23)
    """:obj:`~jce.types.INT64`: large seq."""
    last_watch_start_time: types.INT64 = JceField(0, jce_id=24)
    """:obj:`~jce.types.INT64`: unknown."""
    bind_uin: Optional[types.LIST[types.JceType]] = JceField(None, jce_id=25)
    """:obj:`~jce.types.LIST`: unknown."""
    old_sso_ip: types.INT64 = JceField(0, jce_id=26)
    """:obj:`~jce.types.INT64`: old sso ip."""
    new_sso_ip: types.INT64 = JceField(0, jce_id=27)
    """:obj:`~jce.types.INT64`:  new sso ip."""
    channel_num: types.STRING = JceField("", jce_id=28)
    """:obj:`~jce.types.STRING`: unknown."""
    cp_id: types.INT64 = JceField(0, jce_id=29)
    """:obj:`~jce.types.INT64`: unknown."""
    vendor_name: types.STRING = JceField("", jce_id=30)
    """:obj:`~jce.types.STRING`: vendor name.

    from com.tencent.qphone.base.util.ROMUtil.getRomName():
        MIUI, EMUI, FuntouchOS, SMARTISAN, LENOVO, H2OS/O2OS, EUI, MiFavorUI,
        NUBIAUI, FLYME, LINEAGE, 360, Build.MANUFACTURER
    """
    vendor_os_name: types.STRING = JceField("", jce_id=31)
    """:obj:`~jce.types.STRING`: vendor os name.

    com.tencent.qphone.base.util.ROMUtil.getRomVersion():
        ro.miui.ui.version.name, ro.build.version.emui, ro.vivo.os.version, ...
    """
    ios_idfa: types.STRING = JceField("", jce_id=32)
    """:obj:`~jce.types.STRING`: unknown."""
    b769_req: Optional[types.BYTES] = JceField(None, jce_id=33)
    """:obj:`~jce.types.BYTES`: oidb 0x769 request body."""
    is_set_status: types.BOOL = JceField(jce_id=34)
    """:obj:`~jce.types.BOOL`: is set status.

    reg push reason:
        setOnlineStatus: True, else: False.
    """
    server_buf: Optional[types.BYTES] = JceField(None, jce_id=35)
    """:obj:`~jce.types.BYTES`: unknown."""
    set_mute: types.BOOL = JceField(jce_id=36)
    """:obj:`~jce.types.BOOL`: set mute."""
    ext_online_status: types.INT64 = JceField(jce_id=38)
    """:obj:`~jce.types.INT64`: extra online status."""
    battery_status: types.INT32 = JceField(jce_id=39)
    """:obj:`~jce.types.INT32`: battery status.

    battery capacity ( ``capacity | 128`` when power connect).
    """
    vendor_push_info: Optional[VendorPushInfo] = JceField(None, jce_id=42)
    """:obj:`.VendorPushInfo`: vendor push info."""


class SvcRespRegister(JceStruct):
    """Service Response Register Jce Packet.

    Note:
        Source: com.tencent.msf.service.protocol.push.SvcRespRegister
    """
    uin: types.INT64 = JceField(jce_id=0)
    """:obj:`~jce.types.INT64`: uin."""
    bid: types.INT64 = JceField(jce_id=1)
    """:obj:`~jce.types.INT64`: login bid.

    login: 1 | 2 | 4 = 7, logout: 0.
    """
    reply_code: types.INT8 = JceField(jce_id=2)
    """:obj:`~jce.types.INT8`: reply code."""
    result: types.STRING = JceField("", jce_id=3)
    """:obj:`~jce.types.STRING`: reply message."""
    server_time: types.INT64 = JceField(0, jce_id=4)
    """:obj:`~jce.types.INT64`: server time."""
    log_qq: types.BYTE = JceField(bytes(1), jce_id=5)
    """:obj:`~jce.types.BYTE`: unknown."""
    need_kick: types.BOOL = JceField(False, jce_id=6)
    """:obj:`~jce.types.BOOL`: need kick."""
    update_flag: types.BYTE = JceField(bytes(1), jce_id=7)
    """:obj:`~jce.types.BYTE`: unknown."""
    timestamp: types.INT64 = JceField(0, jce_id=8)
    """:obj:`~jce.types.INT64`: timestamp."""
    crash_flag: types.BYTE = JceField(bytes(1), jce_id=9)
    """:obj:`~jce.types.BYTE`: unknown."""
    client_ip: types.STRING = JceField("", jce_id=10)
    """:obj:`~jce.types.STRING`: client IP."""
    client_port: types.INT = JceField(0, jce_id=11)
    """:obj:`~jce.types.INT`: client port."""
    hello_interval: types.INT = JceField(300, jce_id=12)
    """:obj:`~jce.types.INT`: heartbeat interval time."""
    large_seq: types.INT64 = JceField(jce_id=13)
    """:obj:`~jce.types.INT64`: large seq."""
    large_seq_update: types.BYTE = JceField(bytes(1), jce_id=14)
    """:obj:`~jce.types.BYTE`: unknown."""
    b769_resp: Optional[types.BYTES] = JceField(None, jce_id=15)
    """:obj:`~jce.types.BYTES`: oidb 0x769 response body."""
    status: types.INT32 = JceField(0, jce_id=16)
    """:obj:`~jce.types.INT32`: online status.

    online: 11, offline: 21, away: 31, invisible: 41,
    busy: 50, qme: 60, dnd: 70, receive_offline_msg: 95.
    """
    ext_online_status: types.INT64 = JceField(0, jce_id=17)
    """:obj:`~jce.types.INT64`: extra online status."""
    client_battery_get_interval: types.INT64 = JceField(86400, jce_id=18)
    """:obj:`~jce.types.INT64`: client battery status get interval."""
    client_auto_status_interval: types.INT64 = JceField(600, jce_id=19)
    """:obj:`~jce.types.INT64`: client status get interval."""
