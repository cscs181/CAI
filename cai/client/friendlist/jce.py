"""Friend List Packet Builder.

This module is used to build and handle friend list packets.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional

from jce import JceStruct, JceField, types


class TroopListReqV2(JceStruct):
    """Get Troop(Group) List Request V2 Jce Packet.

    Warning:
        **Not Implemented.**
        Use :obj:`.GetTroopListReqV2Simplify` instead!

    Note:
        Source: friendlist.GetTroopListReqV2
    """


class StTroopNumSimplify(JceStruct):
    """St Troop(Group) Number Simplified Jce Packet.

    Note:
        Source: friendlist.stTroopNumSimplify
    """

    group_code: types.INT64 = JceField(jce_id=0)
    """:obj:`~jce.types.INT64`: group code."""
    group_info_seq: types.INT64 = JceField(jce_id=1)
    """:obj:`~jce.types.INT64`: group info sequence."""
    group_flag_ext: types.INT64 = JceField(jce_id=2)
    """:obj:`~jce.types.INT64`: group flag extension."""
    group_rank_seq: types.INT64 = JceField(jce_id=3)
    """:obj:`~jce.types.INT64`: group rank sequence."""
    group_info_ext_seq: types.INT64 = JceField(jce_id=4)
    """:obj:`~jce.types.INT64`: group info extension sequence."""


class TroopListReqV2Simplify(JceStruct):
    """Get Troop(Group) List Request V2 Simplfied Jce Packet.

    Note:
        Source: friendlist.GetTroopListReqV2Simplify
    """

    uin: types.INT64 = JceField(jce_id=0)
    """:obj:`~jce.types.INT64`: uin."""
    get_msf_msg_flag: types.BOOL = JceField(jce_id=1)
    """:obj:`~jce.types.BOOL`: get msf message or not."""
    cookies: Optional[types.BYTES] = JceField(None, jce_id=2)
    """:obj:`~jce.types.BYTES`: vec cookies."""
    group_info: Optional[types.LIST[StTroopNumSimplify]] = JceField(
        None, jce_id=3
    )
    """:obj:`~jce.types.LIST` of :obj:`.StTroopNumSimplify`: group info."""
    group_flag_ext: types.BYTE = JceField(jce_id=4)
    """:obj:`~jce.types.BYTE`: group flag extension."""
    version: types.INT32 = JceField(jce_id=5)
    """:obj:`~jce.types.INT32`: version."""
    company_id: types.INT64 = JceField(0, jce_id=6)
    """:obj:`~jce.types.INT64`: company id."""
    version_num: types.INT64 = JceField(jce_id=7)
    """:obj:`~jce.types.INT64`: version number."""
    get_long_group_name: types.BOOL = JceField(jce_id=8)
    """:obj:`~jce.types.BOOL`: get long group name or not."""
