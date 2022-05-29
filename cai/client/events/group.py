from dataclasses import dataclass
from typing import Any, Dict, List

from cai.pb.msf.msg.comm import Msg
from cai.client.message import Element

from .base import Event


@dataclass
class GroupEvent(Event):
    group_id: int


# online push push msg
@dataclass
class GroupMessageEvent(GroupEvent):
    _msg: Msg
    seq: int
    time: int
    group_name: str
    group_level: int
    from_uin: int
    from_group_card: str
    message: List[Element]


# online push graytip
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


# online push msg recall
@dataclass
class GroupMessageRecalledEvent(GroupEvent):
    operator_id: int
    author_id: int
    msg_seq: int
    msg_time: int
    msg_type: int
    msg_random: int
    is_anony_msg: bool


# online push general graytip
@dataclass
class _GroupGeneralGrayTipEvent(GroupEvent):
    template_id: int
    template_text: str
    template_params: Dict[str, str]


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
class GroupLuckyCharacterEvent(_GroupGeneralGrayTipEvent):
    @property
    def user_id(self) -> int:
        return int(self.template_params["uin"])

    @property
    def detail_url(self) -> str:
        return self.template_params["detail_url"]


@dataclass
class GroupLuckyCharacterInitEvent(GroupLuckyCharacterEvent):  # 抽中并开启
    @property
    def lucky_character_url(self) -> str:
        return self.template_params["img_url"]


@dataclass
class GroupLuckyCharacterNewEvent(GroupLuckyCharacterEvent):  # 抽中
    @property
    def lucky_character_url(self) -> str:
        return self.template_params["img_url"]


@dataclass
class GroupLuckyCharacterChangedEvent(GroupLuckyCharacterEvent):  # 更换
    @property
    def previous_character_url(self) -> str:
        return self.template_params["img_url_1"]

    @property
    def new_character_url(self) -> str:
        return self.template_params["img_url_2"]


@dataclass
class GroupLuckyCharacterClosedEvent(GroupLuckyCharacterEvent):  # 关闭
    @property
    def lucky_character_url(self) -> str:
        return self.template_params["img_url"]


@dataclass
class GroupLuckyCharacterOpenedEvent(GroupLuckyCharacterEvent):  # 开启
    @property
    def lucky_character_url(self) -> str:
        return self.template_params["img_url"]


@dataclass
class GroupMemberMutedEvent(GroupEvent):
    operator_id: int
    target_id: int
    duration: int


@dataclass
class GroupMemberUnMutedEvent(GroupEvent):
    operator_id: int
    target_id: int
