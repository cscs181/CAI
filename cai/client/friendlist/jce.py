"""Friend List Packet Builder.

This module is used to build and handle friend list packets.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional

from jce import JceStruct, JceField, types


class StTroopNum(JceStruct):
    """St Troop(Group) Number Jce Packet.

    Note:
        Source: friendlist.stTroopNum
    """

    group_uin: types.INT64 = JceField(jce_id=0)
    group_code: types.INT64 = JceField(jce_id=1)
    flag: types.BYTE = JceField(bytes(1), jce_id=2)
    group_info_seq: types.INT64 = JceField(0, jce_id=3)
    group_name: types.STRING = JceField("", jce_id=4)
    group_memo: types.STRING = JceField("", jce_id=5)
    group_flag_ext: types.INT64 = JceField(0, jce_id=6)
    group_rank_seq: types.INT64 = JceField(0, jce_id=7)
    cert_type: types.INT64 = JceField(0, jce_id=8)
    shutup_timestamp: types.INT64 = JceField(0, jce_id=9)
    my_shutup_timestamp: types.INT64 = JceField(0, jce_id=10)
    cmd_uin_uin_flag: types.INT64 = JceField(0, jce_id=11)
    additional_flag: types.INT64 = JceField(0, jce_id=12)
    group_type_flag: types.INT64 = JceField(0, jce_id=13)
    group_sec_type: types.INT64 = JceField(0, jce_id=14)
    group_sec_type_info: types.INT64 = JceField(0, jce_id=15)
    group_class_ext: types.INT64 = JceField(0, jce_id=16)
    app_privilege_flag: types.INT64 = JceField(0, jce_id=17)
    subscription_uin: types.INT64 = JceField(0, jce_id=18)
    member_num: types.INT64 = JceField(0, jce_id=19)
    member_num_seq: types.INT64 = JceField(0, jce_id=20)
    member_card_seq: types.INT64 = JceField(0, jce_id=21)
    group_flag_ext3: types.INT64 = JceField(0, jce_id=22)
    group_owner_uin: types.INT64 = JceField(0, jce_id=23)
    is_conf_group: types.BOOL = JceField(False, jce_id=24)
    is_modify_conf_group_face: types.BOOL = JceField(False, jce_id=25)
    is_modify_conf_group_name: types.BOOL = JceField(False, jce_id=26)
    cmd_uin_join_time: types.INT64 = JceField(0, jce_id=27)
    company_id: types.INT64 = JceField(0, jce_id=28)
    max_group_member_num: types.INT64 = JceField(0, jce_id=29)
    cmd_uin_group_mask: types.INT64 = JceField(0, jce_id=30)
    hl_guild_appid: types.INT64 = JceField(0, jce_id=31)
    hl_guild_sub_type: types.INT64 = JceField(0, jce_id=32)
    cmd_uin_ringtone_id: types.INT64 = JceField(0, jce_id=33)
    cmd_uin_flag_ex2: types.INT64 = JceField(0, jce_id=34)
    group_flag_ext4: types.INT64 = JceField(0, jce_id=35)
    appeal_deadline: types.INT64 = JceField(0, jce_id=36)
    group_flag: types.INT64 = JceField(0, jce_id=37)
    group_remark: types.INT64 = JceField(0, jce_id=38)


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


class StLevelRankPair(JceStruct):
    """St Level Rank Pair Jce Packet.

    Note:
        Source: friendlist.stLevelRankPair
    """

    level: types.INT64 = JceField(jce_id=0)
    rank: types.STRING = JceField(jce_id=1)


class StGroupRankInfo(JceStruct):
    """St Group Rank Info Jce Packet.

    Note:
        Source: friendlist.stGroupRankInfo
    """

    group_code: types.INT64 = JceField(jce_id=0)
    group_rank_sys_flag: types.BYTE = JceField(bytes(1), jce_id=1)
    group_rank_user_flag: types.BYTE = JceField(bytes(1), jce_id=2)
    rank_map: types.LIST[StLevelRankPair] = JceField([], jce_id=3)
    group_rank_seq: types.INT64 = JceField(0, jce_id=4)
    owner_name: types.STRING = JceField("", jce_id=5)
    admin_name: types.STRING = JceField("", jce_id=6)
    office_mode: types.INT64 = JceField(0, jce_id=7)
    group_rank_user_flag_new: types.BYTE = JceField(0, jce_id=8)
    rank_map_new: types.LIST[StLevelRankPair] = JceField([], jce_id=9)


class StFavoriteGroup(JceStruct):
    """St Favorite Group Jce Packet.

    Note:
        Source: friendlist.stFavoriteGroup
    """

    group_code: types.INT64 = JceField(jce_id=0)
    timestamp: types.INT64 = JceField(0, jce_id=1)
    sns_flag: types.INT64 = JceField(0, jce_id=2)
    open_timestamp: types.INT64 = JceField(0, jce_id=3)


class TroopListReqV2(JceStruct):
    """Get Troop(Group) List Request V2 Jce Packet.

    Warning:
        **Not Implemented.**
        Use :obj:`.GetTroopListReqV2Simplify` instead!

    Note:
        Source: friendlist.GetTroopListReqV2
    """


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


class TroopListRespV2(JceStruct):
    uin: types.INT64 = JceField(jce_id=0)
    troop_count: types.INT16 = JceField(jce_id=1)
    result: types.INT32 = JceField(jce_id=2)
    error_code: types.INT16 = JceField(0, jce_id=3)
    cookies: Optional[types.BYTES] = JceField(None, jce_id=4)
    troop_list: types.LIST[StTroopNum] = JceField([], jce_id=5)
    troop_list_del: types.LIST[StTroopNum] = JceField([], jce_id=6)
    troop_list_rank: types.LIST[StGroupRankInfo] = JceField([], jce_id=7)
    favorite_group: types.LIST[StFavoriteGroup] = JceField([], jce_id=8)
    troop_list_ext: types.LIST[StTroopNum] = JceField([], jce_id=9)
    group_info_ext: types.LIST[types.INT64] = JceField([], jce_id=10)
