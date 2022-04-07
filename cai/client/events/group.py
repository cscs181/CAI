from dataclasses import dataclass

from .base import Event


class GroupEvent(Event):
    @property
    def type(self) -> str:
        return self.__class__.__name__


@dataclass
class MemberMutedEvent(GroupEvent):
    group: int
    operator: int
    target: int
    duration: int


@dataclass
class MemberUnMutedEvent(GroupEvent):
    group: int
    operator: int
    target: int


@dataclass
class MemberRecallMessageEvent(GroupEvent):
    group: int
    operator: int
    operator_type: int
    target: int

    msg_rand: int
    msg_seq: int
    msg_time: int

