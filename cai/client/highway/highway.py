import asyncio
import logging
from hashlib import md5
from typing import Tuple, BinaryIO, TYPE_CHECKING

from .decoders import decode_upload_image_resp
from .encoders import encode_d388_req
from .utils import calc_file_md5_and_length, timeit, to_img_id
from .frame import read_frame, write_frame
from cai.pb.highway.protocol.highway_head_pb2 import highway_head
from ..message_service.models import ImageElement

if TYPE_CHECKING:
    from cai.client.client import Client


def _create_highway_header(
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


class HighWaySession:
    def __init__(self, client: "Client", logger: logging.Logger = None):
        if not logger:
            logger = logging.getLogger(__name__)
        self.logger = logger
        self._client = client

    async def upload_image(self, file: BinaryIO, gid: int) -> ImageElement:
        fmd5, fl = calc_file_md5_and_length(file)
        ret = decode_upload_image_resp(
            (await self._client.send_unipkg_and_wait(
                "ImgStore.GroupPicUp",
                encode_d388_req(gid, self._client.uin, fmd5, fl).SerializeToString()
            )).data
        )
        if ret.resultCode != 0:
            raise ConnectionError(ret.resultCode)
        elif not ret.isExists:
            self.logger.debug("file not found, uploading...")

            for addr in ret.uploadAddr:
                try:
                    t, _ = await timeit(
                        self.bdh_uploader(
                            b"PicUp.DataUp",
                            addr,
                            file,
                            2,
                            ret.uploadKey
                        )
                    )
                    self.logger.info("upload complete, use %fs in %d bytes" % (t * 1000, fl))
                except TimeoutError:
                    self.logger.error(f"server {addr[0]}:{addr[1]} timeout")
                    continue
                finally:
                    file.seek(0)
                break
            else:
                raise ConnectionError("cannot upload image, all server failure")

        if ret.hasMetaData:
            image_type = ret.fileType
            w, h = ret.width, ret.height
        else:
            image_type = 1000
            w, h = (800, 600)

        return ImageElement(
            id=ret.fileId,
            filename=to_img_id(fmd5),
            size=fl,
            width=w,
            height=h,
            md5=fmd5,
            filetype=image_type,
            url=f"https://gchat.qpic.cn/gchatpic_new/1/0-0-{fmd5.hex().upper()}/0?term=2"
        )

    async def bdh_uploader(
        self,
        cmd: bytes,
        addr: Tuple[str, int],
        file: BinaryIO,
        cmd_id: int,
        ticket: bytes, *,
        block_size=65535
    ):
        fmd5, fl = calc_file_md5_and_length(file)
        reader, writer = await asyncio.open_connection(*addr)
        bc = 0
        try:
            while True:
                bl = file.read(block_size)
                if not bl:
                    break
                head = highway_head.ReqDataHighwayHead(
                    basehead=_create_highway_header(cmd, 4096, cmd_id, self._client),
                    seghead=highway_head.SegHead(
                        filesize=fl,
                        dataoffset=bc * block_size,
                        datalength=len(bl),
                        serviceticket=ticket,
                        md5=md5(bl).digest(),
                        fileMd5=fmd5
                    )
                ).SerializeToString()

                writer.write(write_frame(head, bl))
                await writer.drain()

                resp, _ = await read_frame(reader)

                bc += 1
        finally:
            writer.close()
