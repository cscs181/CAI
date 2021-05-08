"""QQ Service Packet Builder.

This module is used to build and handle qq service packets.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from jce import JceStruct, JceField, types


class StShareData(JceStruct):
    """Share Data Jce Packet.

    Note:
        Source: QQService.ShareData
    """

    pkg_name: types.STRING = JceField(jce_id=0)
    msgtail: types.STRING = JceField(jce_id=1)
    pic_url: types.STRING = JceField(jce_id=2)
    url: types.STRING = JceField(jce_id=3)


class VipOpenInfo(JceStruct):
    """Vip Open Info Jce Packet.

    Note:
        Source: QQService.VipOpenInfo
    """

    open: types.BOOL = JceField(jce_id=0)
    vip_type: types.INT32 = JceField(jce_id=1)
    vip_level: types.INT32 = JceField(jce_id=2)
    vip_flag: types.INT32 = JceField(0, jce_id=3)
    nameplate_id: types.INT64 = JceField(0, jce_id=4)


class VipBaseInfo(JceStruct):
    """Vip Base Info Jce Packet.

    Note:
        Source: QQService.VipBaseInfo
    """

    open_info: types.MAP[types.INT, VipOpenInfo] = JceField(jce_id=0)
    nameplate_vip_type: types.INT32 = JceField(0, jce_id=1)
    gray_nameplate_flag: types.INT32 = JceField(0, jce_id=2)
    extend_nameplate_id: types.STRING = JceField("", jce_id=3)
