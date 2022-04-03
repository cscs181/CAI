import asyncio
import struct
from typing import Tuple

from cai.pb.highway.protocol.highway_head_pb2 import highway_head


def write_frame(head: bytes, body: bytes) -> bytes:
    buf = bytearray()
    buf.append(0x28)
    buf += struct.pack("!II", len(head), len(body))
    buf += head
    buf += body
    buf.append(0x29)
    return buf


async def read_frame(reader: asyncio.StreamReader) -> Tuple[highway_head.RspDataHighwayHead, bytes]:
    head = await reader.readexactly(9)
    if len(head) != 9 and head[0] != 0x28:
        raise ValueError("Invalid frame head", head)
    hl, bl = struct.unpack("!II", head[1:])
    try:
        return (
            highway_head.RspDataHighwayHead.FromString(await reader.readexactly(hl)),
            await reader.readexactly(bl)
        )
    finally:
        await reader.read(1)  # flush end byte
