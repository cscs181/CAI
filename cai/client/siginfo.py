from typing import Dict

from dataclasses import dataclass, field


@dataclass
class SigInfo:
    login_bitmap: int = 0
    tgt: bytes = bytes()
    tgt_key: bytes = bytes()

    # study room manager | 0x16a
    srm_token: bytes = bytes()
    t133: bytes = bytes()
    encrypted_a1: bytes = bytes()
    user_st_key: bytes = bytes()
    user_st_web_sig: bytes = bytes()
    s_key: bytes = bytes()
    s_key_expire_time: int = 0
    d2: bytes = bytes()
    d2key: bytes = bytes()
    wt_session_ticket_key: bytes = bytes()
    device_token: bytes = bytes()
    ps_key_map: Dict[str, bytes] = field(default_factory=lambda: {})
    pt4_token_map: Dict[str, bytes] = field(default_factory=lambda: {})
