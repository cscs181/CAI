from typing import List
from dataclasses import dataclass

from cai.pb.msf.msg.comm import Msg
from cai.client.message import Element

from .base import Event


@dataclass
class PrivateEvent(Event):
    user_id: int


# message service get message
@dataclass
class PrivateMessageEvent(PrivateEvent):
    _msg: Msg
    seq: int
    time: int
    auto_reply: bool
    user_nick: str
    to_id: int
    message: List[Element]
