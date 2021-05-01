"""Friend List Packet Builder.

This module is used to build and handle friend list packets.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Optional

from jce import JceStruct, JceField, types

from cai.client.qq_service.jce import VipBaseInfo


# Friend
class FriendInfo(JceStruct):
    """Friend Info Jce Packet.

    Note:
        Source: friendlist.FriendInfo
    """

    friend_uin: types.INT64 = JceField(jce_id=0)
    group_id: types.INT8 = JceField(jce_id=1)
    face_id: types.INT16 = JceField(jce_id=2)
    remark: types.STRING = JceField(jce_id=3)
    sqqtype: types.BYTE = JceField(jce_id=4)
    status: types.BYTE = JceField(jce_id=5)
    member_level: types.BYTE = JceField(bytes(1), jce_id=6)
    is_mqq_online: types.BOOL = JceField(False, jce_id=7)
    sqq_online_state: types.BYTE = JceField(bytes(1), jce_id=8)
    is_iphone_online: types.BOOL = JceField(False, jce_id=9)
    detail_status_flag: types.BYTE = JceField(jce_id=10)
    sqq_online_state_v2: types.BYTE = JceField(bytes(1), jce_id=11)
    show_name: types.STRING = JceField("", jce_id=12)
    is_remark: types.BOOL = JceField(False, jce_id=13)
    nick: types.STRING = JceField("", jce_id=14)
    special_flag: types.BYTE = JceField(bytes(1), jce_id=15)
    im_group_id: types.BYTES = JceField(bytes(), jce_id=16)
    msf_group_id: types.BYTES = JceField(bytes(), jce_id=17)
    term_type: types.INT32 = JceField(0, jce_id=18)
    vip_info: Optional[VipBaseInfo] = JceField(None, jce_id=19)
    network: types.BYTE = JceField(bytes(1), jce_id=20)
    ring: types.BYTES = JceField(bytes(), jce_id=21)
    abi_flag: types.INT64 = JceField(0, jce_id=22)
    face_addon_id: types.INT64 = JceField(0, jce_id=23)
    network_type: types.INT32 = JceField(0, jce_id=24)
    vip_font: types.INT64 = JceField(0, jce_id=25)
    icon_type: types.INT32 = JceField(0, jce_id=26)
    term_description: types.STRING = JceField("", jce_id=27)
    color_ring: types.INT64 = JceField(0, jce_id=28)
    apollo_flag: types.BYTE = JceField(bytes(1), jce_id=29)
    apollo_timestamp: types.INT64 = JceField(0, jce_id=30)
    sex: types.INT8 = JceField(0, jce_id=31)
    founder_font: types.INT64 = JceField(0, jce_id=32)
    eim_id: types.STRING = JceField("", jce_id=33)
    eim_mobile: types.STRING = JceField("", jce_id=34)
    olympic_torch: types.BYTE = JceField(bytes(1), jce_id=35)
    apollo_sign_time: types.INT64 = JceField(0, jce_id=36)
    lavi_uin: types.INT64 = JceField(0, jce_id=37)
    tag_update_time: types.INT64 = JceField(0, jce_id=38)
    game_last_login_time: types.INT64 = JceField(0, jce_id=39)
    game_app_id: types.INT64 = JceField(0, jce_id=40)
    card_id: types.BYTES = JceField(bytes(), jce_id=41)
    bit_set: types.INT64 = JceField(0, jce_id=42)
    king_of_glory_flag: types.BYTE = JceField(bytes(1), jce_id=43)
    king_of_glory_rank: types.INT64 = JceField(0, jce_id=44)
    master_uin: types.STRING = JceField("", jce_id=45)
    last_medal_update_time: types.INT64 = JceField(0, jce_id=46)
    face_store_id: types.INT64 = JceField(0, jce_id=47)
    font_effect: types.INT64 = JceField(0, jce_id=48)
    dov_id: types.STRING = JceField("", jce_id=49)
    both_flag: types.INT64 = JceField(0, jce_id=50)
    centi_show_3d_flag: types.BYTE = JceField(bytes(1), jce_id=51)
    intimate_info: types.BYTES = JceField(bytes(), jce_id=52)
    show_nameplate: types.BYTE = JceField(bytes(1), jce_id=53)
    new_lover_diamond_flag: types.BYTE = JceField(bytes(1), jce_id=54)
    ext_sns_friend_data: types.BYTES = JceField(bytes(), jce_id=55)
    mutual_mark_data: types.BYTES = JceField(bytes(), jce_id=56)
    ext_online_status: types.INT64 = JceField(0, jce_id=57)
    battery_status: types.INT64 = JceField(0, jce_id=58)
    music_info: types.BYTES = JceField(bytes(), jce_id=59)
    poi_info: types.BYTES = JceField(bytes(), jce_id=60)
    ext_online_business_info: types.BYTES = JceField(bytes(), jce_id=61)


class GroupInfo(JceStruct):
    """Group Info Jce Packet.

    Note:
        Source: friendlist.GroupInfo
    """

    group_id: types.INT8 = JceField(jce_id=0)
    group_name: types.STRING = JceField(jce_id=1)
    friend_count: types.INT32 = JceField(jce_id=2)
    online_friend_count: types.INT32 = JceField(jce_id=3)
    seq_id: types.BYTE = JceField(bytes(1), jce_id=4)
    sqq_online_count: types.INT32 = JceField(0, jce_id=5)


class FriendListSubSrvRspCode(JceStruct):
    """Friend List Sub Service Response Code Jce Packet.

    Note:
        Source: friendlist.FriendListSubSrvRspCode
    """

    get_mutual_mark_rsp_code: types.INT16 = JceField(0, jce_id=0)
    get_intimate_info_rsp_code: types.INT16 = JceField(0, jce_id=1)


class FriendListReq(JceStruct):
    """Get Friend List Request Jce Packet.

    Note:
        Source: friendlist.GetFriendListReq
    """

    request_type: types.INT32 = JceField(jce_id=0)
    if_reflush: types.BOOL = JceField(jce_id=1)
    uin: types.INT64 = JceField(jce_id=2)
    start_index: types.INT16 = JceField(jce_id=3)
    friend_count: types.INT16 = JceField(jce_id=4)
    group_id: types.BYTE = JceField(jce_id=5)
    if_get_group_info: types.BOOL = JceField(jce_id=6)
    group_start_index: types.INT8 = JceField(jce_id=7)
    group_count: types.INT8 = JceField(jce_id=8)
    if_get_msf_group: types.BOOL = JceField(jce_id=9)
    if_show_term_type: types.BOOL = JceField(jce_id=10)
    version: types.INT64 = JceField(jce_id=11)
    uin_list: Optional[types.LIST[types.INT64]] = JceField(None, jce_id=12)
    app_type: types.INT32 = JceField(0, jce_id=13)
    if_get_dovid: types.BOOL = JceField(False, jce_id=14)
    if_get_both_flag: types.BOOL = JceField(False, jce_id=15)
    d50_req: Optional[types.BYTES] = JceField(None, jce_id=16)
    d6b_req: Optional[types.BYTES] = JceField(None, jce_id=17)
    sns_type_list: Optional[types.LIST[types.INT64]] = JceField(None, jce_id=18)


class FriendListResp(JceStruct):
    """Friend List Response Jce Packet.

    Note:
        Source: friendlist.GetFriendListResp
    """

    request_type: types.INT32 = JceField(jce_id=0)
    if_reflush: types.BOOL = JceField(jce_id=1)
    uin: types.INT64 = JceField(jce_id=2)
    start_index: types.INT16 = JceField(jce_id=3)
    get_friend_count: types.INT16 = JceField(jce_id=4)
    total_friend_count: types.INT16 = JceField(jce_id=5)
    friend_count: types.INT16 = JceField(jce_id=6)
    friend_info: types.LIST[FriendInfo] = JceField(jce_id=7)
    group_id: types.BYTE = JceField(0, jce_id=8)
    if_get_group_info: types.BOOL = JceField(jce_id=9)
    group_start_index: types.INT8 = JceField(0, jce_id=10)
    get_group_count: types.INT8 = JceField(0, jce_id=11)
    total_group_count: types.INT8 = JceField(0, jce_id=12)
    group_count: types.INT8 = JceField(0, jce_id=13)
    group_info: types.LIST[GroupInfo] = JceField([], jce_id=14)
    result: types.INT32 = JceField(jce_id=15)
    error_code: types.INT16 = JceField(0, jce_id=16)
    online_friend_count: types.INT16 = JceField(0, jce_id=17)
    server_time: types.INT64 = JceField(0, jce_id=18)
    sqq_online_count: types.INT16 = JceField(0, jce_id=19)
    msf_group_info: types.LIST[GroupInfo] = JceField([], jce_id=20)
    resp_type: types.BYTE = JceField(bytes(1), jce_id=21)
    has_other_resp_type: types.BOOL = JceField(False, jce_id=22)
    self_info: Optional[FriendInfo] = JceField(None, jce_id=23)
    show_pc_icon: types.BOOL = JceField(False, jce_id=24)
    get_ext_sns_rsp_code: types.INT16 = JceField(0, jce_id=25)
    sub_srv_rsp_code: Optional[FriendListSubSrvRspCode] = JceField(
        None, jce_id=26
    )


# Troop
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
    group_remark: types.BYTES = JceField(bytes(), jce_id=38)


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


# Troop Member
class QzoneUserInfo(JceStruct):
    """Qzone User Info Jce Packet.

    Note:
        Source: friendlist.QzoneUserInfo
    """

    star_state: types.INT32 = JceField(0, jce_id=0)
    extend_info: types.MAP[types.STRING, types.STRING] = JceField({}, jce_id=1)


class StTroopMemberInfo(JceStruct):
    """St Troop(Group) Member Info Jce Packet.

    Note:
        Source: friendlist.stTroopMemberInfo
    """

    member_uin: types.INT64 = JceField(jce_id=0)
    face_id: types.INT16 = JceField(jce_id=1)
    age: types.INT8 = JceField(jce_id=2)
    gender: types.INT8 = JceField(jce_id=3)
    nick: types.STRING = JceField(jce_id=4)
    status: types.BYTE = JceField(jce_id=5)
    show_name: types.STRING = JceField("", jce_id=6)
    name: types.STRING = JceField("", jce_id=8)
    cgender: types.BYTE = JceField(bytes(1), jce_id=9)
    phone: types.STRING = JceField("", jce_id=10)
    email: types.STRING = JceField("", jce_id=11)
    memo: types.STRING = JceField("", jce_id=12)
    auto_remark: types.STRING = JceField("", jce_id=13)
    member_level: types.INT64 = JceField(0, jce_id=14)
    join_time: types.INT64 = JceField(0, jce_id=15)
    last_speak_time: types.INT64 = JceField(0, jce_id=16)
    credit_level: types.INT64 = JceField(0, jce_id=17)
    flag: types.INT64 = JceField(0, jce_id=18)
    flag_ext: types.INT64 = JceField(0, jce_id=19)
    point: types.INT64 = JceField(0, jce_id=20)
    concerned: types.BOOL = JceField(False, jce_id=21)
    shielded: types.BOOL = JceField(False, jce_id=22)
    special_title: types.STRING = JceField("", jce_id=23)
    special_title_expire_time: types.INT64 = JceField(0, jce_id=24)
    bytes_job: types.STRING = JceField("", jce_id=25)
    apollo_flag: types.BYTE = JceField(bytes(1), jce_id=26)
    apollo_timestamp: types.INT64 = JceField(0, jce_id=27)
    global_group_level: types.INT64 = JceField(0, jce_id=28)
    title_id: types.INT64 = JceField(0, jce_id=29)
    shutup_timestamp: types.INT64 = JceField(0, jce_id=30)
    global_group_point: types.INT64 = JceField(0, jce_id=31)
    qzone_user_info: Optional[QzoneUserInfo] = JceField(None, jce_id=32)
    rich_card_name_version: types.BYTE = JceField(bytes(1), jce_id=33)
    vip_type: types.INT64 = JceField(0, jce_id=34)
    vip_level: types.INT64 = JceField(0, jce_id=35)
    big_club_level: types.INT64 = JceField(0, jce_id=36)
    big_club_flag: types.INT64 = JceField(0, jce_id=37)
    nameplate: types.INT64 = JceField(0, jce_id=38)
    group_honor: types.BYTES = JceField(bytes(), jce_id=39)
    vec_name: types.BYTES = JceField(bytes(), jce_id=40)
    rich_flag: types.BYTE = JceField(bytes(1), jce_id=41)


class TroopMemberListReq(JceStruct):
    """Get Troop(Group) Member List Request Jce Packet.

    Note:
        Source: friendlist.GetTroopMemberListReq
    """

    uin: types.INT64 = JceField(jce_id=0)
    group_code: types.INT64 = JceField(jce_id=1)
    next_uin: types.INT64 = JceField(jce_id=2)
    group_uin: types.INT64 = JceField(jce_id=3)
    version: types.INT64 = JceField(jce_id=4)
    request_type: types.INT64 = JceField(0, jce_id=5)
    get_list_appoint_time: types.INT64 = JceField(0, jce_id=6)
    rich_card_name_version: types.BYTE = JceField(bytes(1), jce_id=7)


class TroopMemberListResp(JceStruct):
    """Get Troop(Group) Member List Response Jce Packet.

    Note:
        Source: friendlist.GetTroopMemberListResp
    """

    uin: types.INT64 = JceField(jce_id=0)
    group_code: types.INT64 = JceField(jce_id=1)
    group_uin: types.INT64 = JceField(jce_id=2)
    troop_member: types.LIST[StTroopMemberInfo] = JceField(jce_id=3)
    next_uin: types.INT64 = JceField(jce_id=4)
    result: types.INT32 = JceField(jce_id=5)
    error_code: types.INT16 = JceField(0, jce_id=6)
    office_mode: types.INT64 = JceField(0, jce_id=7)
    next_get_time: types.INT64 = JceField(0, jce_id=8)
