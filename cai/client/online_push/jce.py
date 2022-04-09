"""OnlinePush Packet Builder.

This module is used to build and handle OnlinePush packets.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional

from jce import JceField, JceStruct, types

from cai.client.qq_service.jce import StShareData


class DelMsgInfo(JceStruct):
    """OnlinePush Delete Message Info Packet.

    Note:
        Source: OnlinePushPack.DelMsgInfo
    """

    from_uin: types.INT64 = JceField(jce_id=0)
    msg_time: types.INT64 = JceField(jce_id=1)
    msg_seq: types.INT8 = JceField(jce_id=2)
    msg_cookies: types.BYTES = JceField(bytes(), jce_id=3)
    cmd: types.INT8 = JceField(0, jce_id=4)
    msg_type: types.INT64 = JceField(0, jce_id=5)
    app_id: types.INT64 = JceField(0, jce_id=6)
    send_time: types.INT64 = JceField(0, jce_id=7)
    sso_seq: types.INT32 = JceField(0, jce_id=8)
    sso_ip: types.INT32 = JceField(0, jce_id=9)
    client_ip: types.INT32 = JceField(0, jce_id=10)


class DeviceInfo(JceStruct):
    """OnlinePush Device Info Packet.

    Note:
        Source: OnlinePushPack.DeviceInfo
    """

    net_type: types.BYTE = JceField(bytes(1), jce_id=0)
    dev_type: types.STRING = JceField("", jce_id=1)
    os_ver: types.STRING = JceField("", jce_id=2)
    vendor_name: types.STRING = JceField("", jce_id=3)
    vendor_os_name: types.STRING = JceField("", jce_id=4)
    ios_idfa: types.STRING = JceField("", jce_id=5)


class CPicInfo(JceStruct):
    """MessageSvc Online Push CPic Info jce packet.

    Note:
        Source: OnlinePushPack.CPicInfo
    """

    path: types.BYTES = JceField(jce_id=0)
    host: types.BYTES = JceField(bytes(), jce_id=1)


class TempMsgHead(JceStruct):
    """MessageSvc Online Push Temp Message Head jce packet.

    Note:
        Source: OnlinePushPack.TempMsgHead
    """

    c2c_type: types.INT32 = JceField(0, jce_id=0)
    service_type: types.INT32 = JceField(0, jce_id=1)


class MessageInfo(JceStruct):
    """MessageSvc Online Push Message Info jce packet.

    Note:
        Source: OnlinePushPack.MsgInfo
    """

    from_uin: types.INT64 = JceField(jce_id=0)
    message_time: types.INT64 = JceField(jce_id=1)
    message_type: types.INT16 = JceField(jce_id=2)
    message_seq: types.INT16 = JceField(jce_id=3)
    message: types.STRING = JceField(jce_id=4)
    real_message_time: types.INT32 = JceField(0, jce_id=5)
    vec_message: types.BYTES = JceField(bytes(), jce_id=6)
    app_share_id: types.INT64 = JceField(0, jce_id=7)
    message_cookies: types.BYTES = JceField(bytes(), jce_id=8)
    app_share_cookie: types.BYTES = JceField(bytes(), jce_id=9)
    message_uid: types.INT64 = JceField(0, jce_id=10)
    last_change_time: types.INT64 = JceField(0, jce_id=11)
    cpic_info: types.LIST[CPicInfo] = JceField([], jce_id=12)
    share_data: Optional[StShareData] = JceField(None, jce_id=13)
    from_inst_id: types.INT64 = JceField(0, jce_id=14)
    remark_of_sender: types.BYTES = JceField(bytes(), jce_id=15)
    from_mobile: types.STRING = JceField("", jce_id=16)
    from_name: types.STRING = JceField("", jce_id=17)
    nickname: types.LIST[types.STRING] = JceField([], jce_id=18)
    c2c_temp_msg_head: Optional[TempMsgHead] = JceField(None, jce_id=19)


class UinPairMsg(JceStruct):
    last_read_time: types.INT64 = JceField(0, jce_id=1)
    peer_uin: types.INT64 = JceField(0, jce_id=2)
    msg_completed: types.INT64 = JceField(0, jce_id=3)
    msg_info: Optional[types.LIST[MessageInfo]] = JceField(None, jce_id=4)


class SvcRespPushMsg(JceStruct):
    """OnlinePush Service Push Response Packet.

    Note:
        Source: OnlinePushPack.SvcRespPushMsg
    """

    uin: types.INT64 = JceField(jce_id=0)
    del_infos: types.LIST[DelMsgInfo] = JceField(jce_id=1)
    svrip: types.INT32 = JceField(jce_id=2)
    push_token: Optional[types.BYTES] = JceField(None, jce_id=3)
    service_type: types.INT32 = JceField(0, jce_id=4)
    device_info: Optional[DeviceInfo] = JceField(None, jce_id=5)


class SvcReqPushMsg(JceStruct):
    uin: types.INT64 = JceField(jce_id=0)
    msg_time: types.INT64 = JceField(jce_id=1)
    msg_info: types.LIST[MessageInfo] = JceField(jce_id=2)
    svrip: types.INT32 = JceField(jce_id=3)
    sync_cookie: Optional[types.BYTES] = JceField(None, jce_id=4)
    uinpair_msg: Optional[types.LIST[UinPairMsg]] = JceField(None, jce_id=5)
    preview: Optional[types.MAP[types.STRING, types.BYTES]] = JceField(
        None, jce_id=6
    )
    user_active: types.INT32 = JceField(0, jce_id=7)
    general_flag: types.INT32 = JceField(0, jce_id=12)
