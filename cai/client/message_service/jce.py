"""MessageSvc Packet Builder.

This module is used to build and handle MessageSvc packets.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional

from jce import JceField, JceStruct, types

from cai.client.online_push.jce import MessageInfo


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


# Push Force Offline
class RequestPushForceOffline(JceStruct):
    """MessageSvc Push Force Offline Request jce packet.

    Note:
        Source: PushNotifyPack.RequestPushForceOffline
    """

    uin: types.INT64 = JceField(jce_id=0)
    title: types.STRING = JceField("", jce_id=1)
    tips: types.STRING = JceField("", jce_id=2)
    same_device: types.BOOL = JceField(False, jce_id=3)
