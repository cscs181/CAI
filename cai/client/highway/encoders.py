from cai.pb.im.oidb.cmd0x388.cmd0x388_pb2 import (
    D388ReqBody,
    TryUpImgReq,
    TryUpPttReq,
)


def encode_d388_req(
    group_code: int, uin: int, md5: bytes, size: int, subcmd: int
) -> D388ReqBody:
    img, ptt = None, None
    if subcmd == 1:  # upload img
        fn = md5.hex().upper() + ".jpg"
        img = [
            TryUpImgReq(
                groupCode=group_code,
                srcUin=uin,
                fileName=fn.encode(),
                fileMd5=md5,
                fileSize=size,
                fileId=0,
                srcTerm=5,
                platformType=9,
                buType=1,
                picType=1003,
                picWidth=1920,
                picHeight=903,
                buildVer=b"8.8.50.2324",
                appPicType=1052,
                originalPic=1,
                srvUpload=0,
            )
        ]
    elif subcmd == 3:  # voice
        ptt = [
            TryUpPttReq(
                groupCode=group_code,
                srcUin=uin,
                fileMd5=md5,
                fileName=(md5.hex().upper() + ".amr").encode(),
                fileSize=size,
                voiceLength=size,
                voiceType=1,
                codec=0,
                srcTerm=5,
                platformType=9,
                buType=4,
                innerIp=0,
                buildVer=b"8.8.50.2324",
                newUpChan=True,
            )
        ]
    else:
        ValueError("unsupported subcmd:", subcmd)
    return D388ReqBody(
        netType=8, subcmd=subcmd, tryupImgReq=img, tryupPttReq=ptt
    )
