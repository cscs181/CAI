"""MessageSvc Packet Builder.

This module is used to build and handle MessageSvc packets.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional

from jce import JceStruct, JceField, types

from cai.client.qq_service.jce import StShareData


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


class RequestPushNotify(JceStruct):
    """MessageSvc Push Notify Request jce packet.

    Note:
        Source: PushNotifyPack.RequestPushNotify
    """

    uin: types.INT64 = JceField(jce_id=0)
    type: types.INT8 = JceField(jce_id=1)
    service: types.STRING = JceField(jce_id=2)
    cmd: types.STRING = JceField(jce_id=3)
    notify_cookie: types.BYTES = JceField(bytes(), jce_id=4)
    message_type: types.INT32 = JceField(0, jce_id=5)
    user_active: types.INT32 = JceField(0, jce_id=6)
    general_flag: types.INT32 = JceField(0, jce_id=7)
    binded_uin: types.INT64 = JceField(0, jce_id=8)
    message_info: Optional[MessageInfo] = JceField(None, jce_id=9)
    message_ctrl_buf: types.STRING = JceField("", jce_id=10)
    server_buf: types.BYTES = JceField(bytes(), jce_id=11)
    ping_flag: types.INT64 = JceField(0, jce_id=12)
    svrip: types.INT64 = JceField(0, jce_id=13)


class RequestPushForceOffline(JceStruct):
    """MessageSvc Push Force Offline Request jce packet.

    Note:
        Source: PushNotifyPack.RequestPushForceOffline
    """

    uin: types.INT64 = JceField(jce_id=0)
    title: types.STRING = JceField("", jce_id=1)
    tips: types.STRING = JceField("", jce_id=2)
    same_device: types.BOOL = JceField(False, jce_id=3)
