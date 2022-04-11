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


@dataclass
class _GroupGeneralGrayTipEvent(GroupEvent):
    template_id: int
    template_text: str
    template_params: Dict[str, str]


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
class GroupNudgeEvent(_GroupGeneralGrayTipEvent):
    @property
    def sender_id(self) -> int:
        return int(self.template_params["uin_str1"])

    @property
    def receiver_id(self) -> int:
        return int(self.template_params["uin_str2"])

    @property
    def action_text(self) -> str:
        return self.template_params["action_str"]

    @property
    def action_img(self) -> str:
        return self.template_params["action_img_url"]

    @property
    def suffix_text(self) -> str:
        return self.template_params["suffix_str"]


@dataclass
class MemberMutedEvent(GroupEvent):
    operator: int
    target: int
    duration: int


@dataclass
class MemberUnMutedEvent(GroupEvent):
    operator: int
    target: int
