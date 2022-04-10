from dataclasses import dataclass
from typing import Any, Dict, List

from .base import Event


@dataclass
class GroupEvent(Event):
    group_id: int

    @property
    def type(self) -> str:
        return self.__class__.__name__


@dataclass
class _GroupGrayTipEvent(GroupEvent):
    text: str
    raw_text: str
    cmds: List[Dict[str, Any]]


# FIXME: unhandle details
@dataclass
class GroupRedbagEvent(GroupEvent):
    sender_id: int


@dataclass
class GroupMemberSpecialTitleChangedEvent(_GroupGrayTipEvent):
    user_id: int


@dataclass
class GroupNameChangedEvent(_GroupGrayTipEvent):
    ...


@dataclass
class GroupMessageRecalledEvent(GroupEvent):
    operator_id: int
    author_id: int
    msg_seq: int
    msg_time: int
    msg_type: int
    msg_random: int
    is_anony_msg: bool


@dataclass
class MemberMutedEvent(GroupEvent):
    operator: int
    target: int
    duration: int


@dataclass
class MemberUnMutedEvent(GroupEvent):
    operator: int
    target: int
