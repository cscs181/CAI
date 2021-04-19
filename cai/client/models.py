"""Application Client Info Releated Models.

This module is used to define account info data models.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import time
from typing import Dict
from dataclasses import dataclass, field

from cai.utils.dataclass import JsonableDataclass


@dataclass
class SigInfo:
    """Account Siginfo.

    Note:
        Source: oicq.wlogin_sdk.sharemem.WloginSigInfo
    """

    d2: bytes = bytes()
    d2key: bytes = bytes()

    g: bytes = bytes()
    tgt: bytes = bytes()
    tgt_key: bytes = bytes()
    device_token: bytes = bytes()
    dpwd: bytes = bytes()
    no_pic_sig: bytes = bytes()
    encrypted_a1: bytes = bytes()
    login_bitmap: int = 0
    ps_key_map: Dict[str, bytes] = field(default_factory=lambda: {})
    pt4_token_map: Dict[str, bytes] = field(default_factory=lambda: {})
    rand_seed: bytes = bytes()
    _s_key: bytes = bytes()
    s_key_expire_time: int = 0
    user_st_key: bytes = bytes()
    user_st_web_sig: bytes = bytes()
    wt_session_ticket: bytes = bytes()
    wt_session_ticket_key: bytes = bytes()

    @property
    def s_key(self) -> bytes:
        return self._s_key

    @s_key.setter
    def s_key(self, value: bytes):
        self._s_key = value
        self.s_key_expire_time = int(time.time()) + 21600


@dataclass
class Friend(JsonableDataclass):
    friend_uin: int
    group_id: int
    face_id: int
    remark: str
    is_mqq_online: bool
    is_iphone_online: bool
    show_name: str
    is_remark: bool
    nick: str
    # vip_info
    network_type: int
    vip_font: int
    term_description: str
    sex: int
    battery_status: int


@dataclass
class Group(JsonableDataclass):
    group_uin: int
    group_code: int
    group_name: str
    group_memo: str
    shutup_timestamp: int
    my_shutup_timestamp: int
    member_num: int
    group_owner_uin: int
    cmd_uin_join_time: int
    max_group_member_num: int

    @property
    def group_id(self) -> int:
        """:obj:`int`: Group ID. Same as :obj:`~.Group.group_uin`."""
        return self.group_uin

    @property
    def join_time(self) -> int:
        """:obj:`int`: Group join time. Same as :obj:`~.Group.cmd_uin_join_time`."""
        return self.cmd_uin_join_time
