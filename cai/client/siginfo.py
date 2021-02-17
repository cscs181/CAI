from dataclasses import dataclass


@dataclass
class SigInfo:
    d2key: bytes = bytes()
    wt_session_ticket_key: bytes = bytes()
