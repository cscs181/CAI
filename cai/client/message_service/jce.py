"""MessageSvc Packet Builder.

This module is used to build and handle MessageSvc packets.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional

from jce import JceStruct, JceField, types


class RequestPushForceOffline(JceStruct):
    """MessageSvc Request Push Force Offline jce packet.

    Note:
        Source: PushNotifyPack.RequestPushForceOffline
    """

    uin: types.INT64 = JceField(jce_id=0)
    title: types.STRING = JceField("", jce_id=1)
    tips: types.STRING = JceField("", jce_id=2)
    same_device: types.BOOL = JceField(False, jce_id=3)
