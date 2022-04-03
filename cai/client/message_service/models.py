"""MessageSvc message models.

This module is used to define message models.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

import abc
from dataclasses import dataclass
from typing import List, Optional

from cai.client.event import Event
from cai.pb.msf.msg.comm import Msg


@dataclass
class PrivateMessage(Event):
    _msg: Msg
    seq: int
    time: int
    auto_reply: bool
    from_uin: int
    from_nick: str
    to_uin: int
    message: List["Element"]

    @property
    def type(self) -> str:
        return "private_message"


@dataclass
class GroupMessage(Event):
    _msg: Msg
    seq: int
    time: int
    group_id: int
    group_name: str
    group_level: int
    from_uin: int
    from_group_card: str
    message: List["Element"]

    @property
    def type(self) -> str:
        return "group_message"


class Element(abc.ABC):
    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedError


@dataclass
class ReplyElement(Element):
    seq: int
    time: int
    sender: int
    message: List[Element]
    troop_name: Optional[str]

    @property
    def type(self) -> str:
        return "reply"


@dataclass
class TextElement(Element):
    content: str

    @property
    def type(self) -> str:
        return "text"


@dataclass
class FaceElement(Element):
    id: int

    @property
    def type(self) -> str:
        return "face"


@dataclass
class SmallEmojiElement(Element):
    id: int
    text: str
    # byte: bytes

    @property
    def type(self) -> str:
        return "small_emoji"


@dataclass
class ImageElement(Element):
    filename: str
    size: int
    width: int
    height: int
    md5: bytes
    id: Optional[int] = -1
    url: Optional[str] = None
    filetype: Optional[int] = 1000

    @property
    def type(self) -> str:
        return "image"


@dataclass
class FlashImageElement(ImageElement):
    @property
    def type(self) -> str:
        return "flash_image"


@dataclass
class PokeElement(Element):
    id: int
    name: str
    strength: int
    double_hit: int

    @property
    def type(self) -> str:
        return "poke"


@dataclass
class AtElement(Element):
    target: int
    display: Optional[str] = ""

    @property
    def type(self) -> str:
        return "at"


@dataclass
class RichMsgElement(Element):
    """
    service_id:
      case -1:
        json
      case -2:
        light_app
      default:
        xml
    """
    content: bytes
    service_id: Optional[int] = -1

    @property
    def type(self) -> str:
        return "rich_msg"
