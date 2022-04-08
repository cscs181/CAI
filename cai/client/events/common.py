from typing import Optional
from dataclasses import dataclass

from .base import Event


@dataclass
class NudgeEvent(Event):
    sender: int
    target: int
    action: str
    suffix: Optional[str]
    group: Optional[int] = None

    @property
    def type(self) -> str:
        return "NudgeEvent"
