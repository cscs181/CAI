import asyncio
import logging
from hashlib import md5
from typing import TYPE_CHECKING, List, Tuple, BinaryIO, Optional

from cai.utils.image import decoder
from cai.pb.highway.protocol.highway_head_pb2 import highway_head

from .encoders import encode_upload_img_req, encode_upload_voice_req
from .frame import read_frame, write_frame
from .utils import to_id, timeit, calc_file_md5_and_length
from ..message.models import ImageElement, VoiceElement
from .decoders import decode_upload_ptt_resp, decode_upload_image_resp

if TYPE_CHECKING:
    from cai.client.client import Client


def _create_highway_header(
    cmd: bytes, flag: int, cmd_id: int, client: "Client", locale=2052
) -> highway_head.DataHighwayHead:
    return highway_head.DataHighwayHead(
        version=1,
        uin=str(client.uin).encode(),
        command=cmd,
        commandId=cmd_id,
        seq=client.next_seq(),
        appid=client.apk_info.sub_app_id,
        localeId=locale,
        dataflag=flag,
    )


class HighWaySession:
    def __init__(self, client: "Client", logger: logging.Logger = None):
        if not logger:
            logger = logging.getLogger(__name__)
        self.logger = logger
        self._client = client
        self._session_sig: Optional[bytes] = None
        self._session_key: Optional[bytes] = None
        self._session_addr_list: Optional[List[Tuple[str, int]]] = []

    def _decode_bdh_session(self):
        info = self._client._file_storage_info
        if not info:
            raise ValueError("info not found, try again later")
        self._session_sig = info.big_data_channel.bigdata_sig_session
        self._session_key = info.big_data_channel.bigdata_key_session
        for iplist in info.big_data_channel.bigdata_iplists:
            for ip in iplist.ip_list:
                self._session_addr_list.append((ip.ip, ip.port))

    async def _upload_controller(
        self,
        addrs: List[Tuple[str, int]],
        file: BinaryIO,
        cmd_id: int,
        ticket: bytes,
        ext=None,
    ) -> Optional[bytes]:
        for addr in addrs:
            try:
                t, d = await timeit(
                    self.bdh_uploader(
                        b"PicUp.DataUp", addr, file, cmd_id, ticket, ext
                    )
                )
                self.logger.info("upload complete, use %fms" % (t * 1000))
                return d
            except TimeoutError:
                self.logger.error(f"server {addr[0]}:{addr[1]} timeout")
                continue
            finally:
                file.seek(0)
        else:
            raise ConnectionError("cannot upload, all server failure")

    async def upload_image(self, file: BinaryIO, gid: int) -> ImageElement:
        fmd5, fl = calc_file_md5_and_length(file)
        info = decoder.decode(file)
        ret = decode_upload_image_resp(
            (
                await self._client.send_unipkg_and_wait(
                    "ImgStore.GroupPicUp",
                    encode_upload_img_req(gid, self._client.uin, fmd5, fl, info).SerializeToString(),
                )
            ).data
        )
        if ret.resultCode != 0:
            raise ConnectionError(ret.resultCode)
        elif not ret.isExists:
            self.logger.debug("file not found, uploading...")

            await self._upload_controller(
                ret.uploadAddr, file, 2, ret.uploadKey  # send to group
            )

        if ret.hasMetaData:
            image_type = ret.fileType
            w, h = ret.width, ret.height
        else:
            image_type = info.pic_type
            w, h = info.width, info.height

        return ImageElement(
            id=ret.fileId,
            filename=to_id(fmd5) + f".{info.name}",
            size=fl,
            width=w,
            height=h,
            md5=fmd5,
            filetype=image_type,
            url=f"https://gchat.qpic.cn/gchatpic_new/1/0-0-{fmd5.hex().upper()}/0?term=2",
        )

    async def upload_voice(self, file: BinaryIO, gid: int) -> VoiceElement:
        fmd5, fl = calc_file_md5_and_length(file)
        ext = encode_upload_voice_req(
            gid, self._client.uin, fmd5, fl
        ).SerializeToString()
        if not (self._session_key and self._session_sig):
            self._decode_bdh_session()
        ret = decode_upload_ptt_resp(
            await self._upload_controller(
                self._session_addr_list,
                file,
                29,  # send to group
                self._session_sig,
                ext,
            )
        )
        if ret.resultCode:
            raise ConnectionError(ret.resultCode, ret.message)
        return VoiceElement(
            to_id(fmd5) + ".amr",
            file_type=4,
            from_uin=self._client.uin,
            md5=fmd5,
            size=fl,
            group_file_key=ret.uploadKey,
            url=f"https://grouptalk.c2c.qq.com/?ver=0&rkey={ret.uploadKey.hex()}&filetype=4%voice_codec=0",
        )

    async def bdh_uploader(
        self,
        cmd: bytes,
        addr: Tuple[str, int],
        file: BinaryIO,
        cmd_id: int,
        ticket: bytes,
        ext: bytes = None,
        *,
        block_size=65535,
    ) -> Optional[bytes]:
        fmd5, fl = calc_file_md5_and_length(file)
        reader, writer = await asyncio.open_connection(*addr)
        bc = 0
        try:
            while True:
                bl = file.read(block_size)
                if not bl:
                    return ext
                head = highway_head.ReqDataHighwayHead(
                    basehead=_create_highway_header(
                        cmd, 4096, cmd_id, self._client
                    ),
                    seghead=highway_head.SegHead(
                        filesize=fl,
                        dataoffset=bc * block_size,
                        datalength=len(bl),
                        serviceticket=ticket,
                        md5=md5(bl).digest(),
                        fileMd5=fmd5,
                    ),
                    reqExtendinfo=ext,
                )

                writer.write(write_frame(head.SerializeToString(), bl))
                await writer.drain()

                resp, data = await read_frame(reader)
                if resp.errorCode:
                    raise ConnectionError(resp.errorCode, "upload error", resp)
                if resp and ext:
                    if resp.rspExtendinfo:
                        ext = resp.rspExtendinfo
                    if resp.seghead:
                        if resp.seghead.serviceticket:
                            self._session_key = resp.seghead.serviceticket

                bc += 1
        finally:
            writer.close()
