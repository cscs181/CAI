import asyncio
import ipaddress
import struct
import uuid
from dataclasses import dataclass
from hashlib import md5
from typing import Tuple, BinaryIO, TYPE_CHECKING, Optional

from cai.client.message_service.models import ImageElement
from cai.utils.gcode import GroupIdConvertor
from cai.client.message_service.upload import encode_d388_req, decode_d388_rsp
from cai.pb.highway.protocol.highway_head_pb2 import highway_head

if TYPE_CHECKING:
    from cai.client.client import Client


# https://github.com/Mrs4s/MiraiGo/blob/master/client/internal/highway/highway.go#L79


def calc_file_md5_and_length(file: BinaryIO, bs=4096) -> Tuple[bytes, int]:
    try:
        fm, length = md5(), 0
        while True:
            bl = file.read(bs)
            fm.update(bl)
            if len(bl) != bs:
                break
            else:
                length += len(bl)
        return fm.digest(), length
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
        uin=str(client.uin).encode(),
        command=cmd,
        commandId=cmd_id,
        seq=client.next_seq(),
        appid=client.apk_info.app_id,
        localeId=locale,
        dataflag=flag
    )


def itoa(i: int) -> str:  # int to address(str)
    return ipaddress.IPv4Address(i).compressed


def to_img_id(i_uuid: int) -> str:
    return "{%s}.png" % uuid.UUID(int=i_uuid)


def write_frame(head: bytes, body: bytes) -> bytes:
    buf = bytearray()
    buf.append(0x28)
    buf += struct.pack("!II", len(head), len(body))
    buf += head
    buf += body
    buf.append(0x29)
    return buf


async def read_frame(reader: asyncio.StreamReader) -> Tuple[highway_head.RspDataHighwayHead, bytes]:
    head = await reader.read(9)
    if len(head) != 9:
        raise ValueError("Invalid frame head", head)
    _, hl, bl = struct.unpack("!cII", head)
    return (
        highway_head.RspDataHighwayHead.FromString(await reader.readexactly(hl)),
        await reader.readexactly(bl)
    )


@dataclass
class ImageUploadResponse:
    uploadKey: Optional[bytes] = None
    uploadIp: Optional[int] = None
    uploadPort: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    message: Optional[str] = None
    downloadIndex: Optional[str] = None
    resourceId: Optional[int] = None
    fileId: Optional[int] = None
    fileType: Optional[int] = None
    resultCode: Optional[int] = 0
    isExists: bool = False
    hasMetaData: bool = False


def decode_upload_image_resp(data: bytes) -> ImageUploadResponse:
    pkg = decode_d388_rsp(data).tryupImgRsp[0]
    if pkg.result != 0:
        return ImageUploadResponse(resultCode=pkg.result, message=pkg.failMsg.decode())

    if pkg.fileExit:
        if pkg.imgInfo:
            info = pkg.imgInfo
            return ImageUploadResponse(
                isExists=True, fileId=pkg.fileId, hasMetaData=True,
                fileType=info.fileType, width=info.fileWidth, height=info.fileHeight
            )
        else:
            return ImageUploadResponse(isExists=True, fileId=pkg.fileId)
    return ImageUploadResponse(
        isExists=False,
        uploadIp=pkg.upIp[0],  # todo: parse
        uploadPort=pkg.upPort[0],
        uploadKey=pkg.upUkey
    )


async def upload_image(file: BinaryIO, gid: int, client: "Client") -> ImageElement:
    fmd5, fl = calc_file_md5_and_length(file)
    ret = decode_upload_image_resp(
        (await client.send_unipkg_and_wait(
            "ImgStore.GroupPicUp",
            encode_d388_req(GroupIdConvertor.to_group_code(gid), client.uin, fmd5, fl, client.apk_info.version.encode()).SerializeToString()
        )).data
    )
    print(ret)
    if ret.resultCode != 0:
        raise ConnectionError(ret.resultCode)
    elif not ret.isExists:
        print("not exists")
        #raise ValueError("Upload Error")

    await bdh_uploader(
        b"PicUp.DataUp",
        (itoa(ret.uploadIp), ret.uploadPort),
        file,
        2,
        ret.uploadKey,
        client
    )
    file.seek(0)

    if ret.hasMetaData:
        image_type = ret.fileType
        w, h = ret.width, ret.height
    else:
        image_type = 1000
        w, h = (800, 600)

    return ImageElement(
        id=ret.fileId,
        filename=to_img_id(ret.fileId),
        size=fl,
        width=w,
        height=h,
        md5=fmd5,
        filetype=image_type,
        url=f"https://gchat.qpic.cn/gchatpic_new/1/0-0-{fmd5:x}/0?term=2"
    )


async def bdh_uploader(
    cmd: bytes,
    addr: Tuple[str, int],
    file: BinaryIO,
    cmd_id: int,
    ticket: bytes,
    client: "Client", *,
    block_size=65535
):
    fmd5, fl = calc_file_md5_and_length(file)
    print(addr)
    reader, writer = await asyncio.open_connection(*addr)
    bc = 0
    while True:
        bl = file.read(block_size)
        if not bl:
            break
        head = highway_head.ReqDataHighwayHead(
            basehead=create_highway_header(cmd, 4096, cmd_id, client),
            seghead=highway_head.SegHead(
                filesize=fl,
                dataoffset=bc * block_size,
                datalength=len(bl),
                serviceticket=ticket,
                # todo: https://github.com/Mrs4s/MiraiGo/blob/38990f6e1cf9ca0785709d03b66237a713338d0b/client/group_msg.go#L216
                md5=md5(bl).digest(),
                fileMd5=fmd5
            )
        ).SerializeToString()

        writer.write(write_frame(head, bl))
        await writer.drain()

        resp, _ = await read_frame(reader)

        bc += 1
