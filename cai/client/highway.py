import asyncio
from hashlib import md5
from typing import Tuple, BinaryIO, TYPE_CHECKING

from cai.pb.highway.protocol.highway_head_pb2 import highway_head

if TYPE_CHECKING:
    from cai.client.client import Client

# https://github.com/Mrs4s/MiraiGo/blob/master/client/internal/highway/highway.go#L79


def calc_file_md5(file: BinaryIO, bs=4096) -> str:
    try:
        fm = md5()
        while True:
            bl = file.read(bs)
            fm.update(bl)
            if len(bl) != bs:
                break
        return fm.hexdigest()
    finally:
        file.seek(0)


def create_highway_header(
    cmd: bytes,
    flag: int,
    cmd_id: int,
    client: "Client",
    locale=2052
) -> highway_head.DataHighwayHead:
    return highway_head.DataHighwayHead(
        version=1,
        uin=bytes(str(client.uin)),
        command=cmd,
        commandId=cmd_id,
        seq=client.next_seq(),
        appid=client.apk_info.app_id,
        localeId=locale,
        dataflag=flag
    )


async def upload_file(addr: Tuple[str, int], file: BinaryIO, cmd_id: int, client: Client, *, block_size=65535):
    fmd5, fl = calc_file_md5(file), len(file.read())
    file.seek(0)
    reader, writer = await asyncio.open_connection(*addr)
    bc = 0
    while True:
        bl = file.read(block_size)
        if not bl:
            break
        highway_head.ReqDataHighwayHead(
            basehead=create_highway_header(b"PicUp.DataUp", 4096, cmd_id, client),
            seghead=highway_head.SegHead(
                filesize=fl,
                dataoffset=bc * block_size,
                datalength=len(bl),
                serviceticket=None,  #todo: https://github.com/Mrs4s/MiraiGo/blob/38990f6e1cf9ca0785709d03b66237a713338d0b/client/group_msg.go#L216

            )
        )
        bc += 1
