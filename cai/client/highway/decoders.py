from .models import ImageUploadResponse, UploadResponse
from .utils import itoa
from cai.pb.im.oidb.cmd0x388.cmd0x388_pb2 import D388RspBody


def decode_upload_image_resp(data: bytes) -> ImageUploadResponse:
    pkg = decode_d388_rsp(data).tryupImgRsp[0]
    if pkg.result != 0:
        return ImageUploadResponse(resultCode=pkg.result, message=pkg.failMsg.decode())

    if pkg.fileExit:
        if pkg.imgInfo:
            info = pkg.imgInfo
            # fuck: pkg.fileId != pkg.fileid
            return ImageUploadResponse(
                isExists=True, fileId=pkg.fileid, hasMetaData=True,
                fileType=info.fileType, width=info.fileWidth, height=info.fileHeight
            )
        else:
            return ImageUploadResponse(isExists=True, fileId=pkg.fileid)
    return ImageUploadResponse(
        isExists=False,
        uploadAddr=[(itoa(a), p) for a, p in zip(pkg.upIp, pkg.upPort)],
        uploadKey=pkg.upUkey
    )


def decode_upload_ptt_resp(data: bytes) -> UploadResponse:
    pkg = decode_d388_rsp(data).tryupPttRsp[0]
    if pkg.result != 0:
        return UploadResponse(resultCode=pkg.result, message=pkg.failMsg.decode())

    if pkg.fileExit:
        return UploadResponse(isExists=True, fileId=pkg.fileid)
    return UploadResponse(
        isExists=False,
        uploadAddr=[(itoa(a), p) for a, p in zip(pkg.upIp, pkg.upPort)],
        uploadKey=pkg.upUkey
    )


def decode_d388_rsp(data: bytes) -> D388RspBody:
    return D388RspBody.FromString(data)
