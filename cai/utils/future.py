import asyncio
from typing import Any, Dict, Generic, TypeVar, Optional, Callable

KT = TypeVar("KT")


class FutureStore(Generic[KT]):

    def __init__(self):
        self._futures: Dict[KT, asyncio.Future] = {}

    def store_seq(self, seq: KT) -> asyncio.Future:
        if seq in self._futures:
            raise KeyError(f"Sequence {seq} already exists!")

        future = asyncio.get_event_loop().create_future()
        self._futures[seq] = future
        return future

    def store_result(self, seq: KT, result: Any):
        future = self._futures.get(seq)
        if future and not future.cancelled():
            future.set_result(result)

    def pop_seq(self, seq: KT) -> asyncio.Future:
        return self._futures.pop(seq)

    def add_callback(self, seq: KT, callback: Callable[[asyncio.Future], Any]):
        future = self._futures[seq]
        future.add_done_callback(callback)

    def remove_callback(
        self, seq: KT, callback: Callable[[asyncio.Future], Any]
    ) -> int:
        future = self._futures[seq]
        return future.remove_done_callback(callback)

    def result(self, seq: KT) -> Any:
        return self._futures[seq].result()

    def cancel(self, seq: KT) -> bool:
        return self._futures[seq].cancel()

    def exception(self, seq: KT):
        return self._futures[seq].exception()

    async def fetch(self, seq: KT, timeout: Optional[float] = None) -> Any:
        future = self.store_seq(
            seq
        ) if seq not in self._futures else self._futures[seq]
        try:
            return await asyncio.wait_for(future, timeout)
        finally:
            del self._futures[seq]
