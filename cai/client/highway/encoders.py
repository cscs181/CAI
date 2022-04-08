from cai.pb.im.cs.cmd0x388 import ReqBody, TryUpImgReq, TryUpPttReq


def encode_d388_req(
    group_code: int, uin: int, md5: bytes, size: int, subcmd: int
) -> ReqBody:
    img, ptt = None, None
    if subcmd == 1:  # upload img
        fn = md5.hex().upper() + ".jpg"
        img = [
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
                pic_type=1003,
                pic_width=1920,
                pic_height=903,
                build_ver=b"8.8.50.2324",
                app_pic_type=1052,
                original_pic=1,
                srv_upload=0,
            )
        ]
    elif subcmd == 3:  # voice
        ptt = [
            TryUpPttReq(
                group_code=group_code,
                src_uin=uin,
                file_md5=md5,
                file_name=(md5.hex().upper() + ".amr").encode(),
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
    else:
        ValueError("unsupported subcmd:", subcmd)
    return ReqBody(
        net_type=8, subcmd=subcmd, tryup_img_req=img, tryup_ptt_req=ptt
    )
