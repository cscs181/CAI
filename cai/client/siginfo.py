"""Application Client SigInfo.

This module is used to define account siginfo data.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import time
from typing import Dict

from dataclasses import dataclass, field


@dataclass
class SigInfo:
    """
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
