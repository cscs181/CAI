import time
import uuid
from hashlib import md5
from typing import BinaryIO, Tuple, Awaitable, Any


def calc_file_md5_and_length(file: BinaryIO, bs=4096) -> Tuple[bytes, int]:
    try:
        fm, length = md5(), 0
        while True:
            bl = file.read(bs)
            fm.update(bl)
            length += len(bl)
            if len(bl) != bs:
                break
        return fm.digest(), length
    finally:
        file.seek(0)


def itoa(i: int) -> str:  # int to address(str)
    return ".".join([str(p) for p in i.to_bytes(4, "little")])


def to_id(b_uuid: bytes) -> str:
    return "{%s}" % uuid.UUID(bytes=b_uuid)


async def timeit(func: Awaitable) -> Tuple[float, Any]:
    start = time.time()
    result = await func
    return time.time() - start, result
