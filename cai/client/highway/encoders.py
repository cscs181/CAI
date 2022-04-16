from cai.pb.im.cs.cmd0x388 import ReqBody, TryUpImgReq, TryUpPttReq
from typing import Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from cai.utils.image.decoder import ImageInfo


def encode_d388_req(
    subcmd: int,
    tryup_img: Sequence[TryUpImgReq] = None,
    tryup_ptt: Sequence[TryUpPttReq] = None
) -> ReqBody:
    return ReqBody(
        net_type=8,
        subcmd=subcmd,
        tryup_img_req=tryup_img,
        tryup_ptt_req=tryup_ptt
    )


def encode_upload_img_req(
    group_code: int,
    uin: int,
    md5: bytes,
    size: int,
    info: "ImageInfo"
) -> ReqBody:
    fn = f"{md5.hex().upper()}.{info.name or 'jpg'}"
    return encode_d388_req(
        subcmd=1,
        tryup_img=[
            TryUpImgReq(
                group_code=group_code,
                src_uin=uin,
                file_name=fn.encode(),
                file_md5=md5,
                file_size=size,
                file_id=0,
                src_term=5,
                platform_type=9,
                bu_type=1,
                pic_type=info.pic_type.value,
                pic_width=info.width,
                pic_height=info.height,
                build_ver=b"8.8.50.2324",
                app_pic_type=1052,
                original_pic=1,
                srv_upload=0,
            )
        ]
    )


def encode_upload_voice_req(
    group_code: int,
    uin: int,
    md5: bytes,
    size: int,
    suffix: str = None,
) -> ReqBody:
    return encode_d388_req(
        subcmd=3,
        tryup_ptt=[
            TryUpPttReq(
                group_code=group_code,
                src_uin=uin,
                file_md5=md5,
                file_name=f"{md5.hex().upper()}.{'amr' if not suffix else suffix}".encode(),
                file_size=size,
                voice_length=size,
                voice_type=1,
                codec=0,
                src_term=5,
                platform_type=9,
                bu_type=4,
                inner_ip=0,
                build_ver=b"8.8.50.2324",
                new_up_chan=True,
            )
        ]
    )
