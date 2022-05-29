"""Coroutine Related Tools

This module is used to build coroutine related tools.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
from types import TracebackType
from collections.abc import Coroutine
from typing import AsyncContextManager
from typing import Coroutine as CoroutineGeneric
from typing import Type, Generic, TypeVar, Optional

TY = TypeVar("TY")
TS = TypeVar("TS")
TR = TypeVar("TR", bound=AsyncContextManager)


class ContextManager(Coroutine, Generic[TY, TS, TR]):

    __slots__ = ("_coro", "_obj")

    def __init__(self, coro: CoroutineGeneric[TY, TS, TR]):
        self._coro = coro
        self._obj: Optional[TR] = None

    def send(self, value: TS) -> TY:
        return self._coro.send(value)

    def throw(self, typ, val=None, tb=None):
        if val is None:
            return self._coro.throw(typ)
        elif tb is None:
            return self._coro.throw(typ, val)
        else:
            return self._coro.throw(typ, val, tb)

    def close(self):
        return self._coro.close()

    def __next__(self):
        raise StopIteration

    def __iter__(self):
        return self._coro.__await__()

    def __await__(self):
        return self._coro.__await__()

    async def __aenter__(self) -> TR:
        self._obj = await self._coro
        return self._obj

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        await self._obj.__aexit__(exc_type, exc_value, traceback)  # type: ignore
        self._obj = None
