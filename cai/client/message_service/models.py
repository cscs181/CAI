"""MessageSvc message models.

This module is used to define message models.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

import abc
from dataclasses import dataclass


@dataclass
class Message:
    type: str


class Element(abc.ABC):
    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedError


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
    byte: bytes

    @property
    def type(self) -> str:
        return "small_emoji"
