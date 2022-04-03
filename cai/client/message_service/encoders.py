import random
import zlib

from typing import Sequence, Union
from cai.pb.im.msg.msg_body import MsgBody, PlainText, RichText, CustomFace, Elem, CommonElem, LightAppElem, RichMsg
from cai.pb.msf.msg.svc.svc_pb2 import RoutingHead, Grp
from cai.pb.msf.msg.comm.comm_pb2 import ContentHead

from . import models
from cai.pb.msf.msg.svc import PbSendMsgReq


# todo: https://github.com/mamoe/mirai/blob/7d3971259de59cede94b7a55650c8a6ad4346a59/mirai-core/src/commonMain/kotlin/network/protocol/packet/chat/receive/MessageSvc.PbSendMsg.kt#L103
# https://github.com/mamoe/mirai/blob/74fc5a50376ed0330b984af51e0fabc2147afdbb/mirai-core/src/commonMain/kotlin/contact/SendMessageHandler.kt


def _build_image_elem(e: Union[models.ImageElement, models.FlashImageElement]) -> CustomFace:
    return CustomFace(
        file_type=66,
        useful=1,
        biz_type=0,
        width=e.width,
        height=e.height,
        file_id=e.id,
        file_path=e.filename,
        image_type=e.filetype,
        source=200,
        origin=1,
        size=e.size,
        md5=e.md5,
        show_len=0,
        download_len=0
        #flag=b"\x00\x00\x00\x00"
    )


def build_msg(elements: Sequence[models.Element]) -> MsgBody:
    ret = []
    for e in elements:  # todo: support more element
        if isinstance(e, models.TextElement):
            ret.append(
                Elem(text=PlainText(str=e.content.encode()))
            )
        elif isinstance(e, models.ImageElement):
            ret.append(
                Elem(
                    custom_face=_build_image_elem(e)
                )
            )
        elif isinstance(e, models.FlashImageElement):
            ret.append(
                Elem(
                    common_elem=CommonElem(
                        service_type=3,
                        pb_elem=_build_image_elem(e).SerializeToString()
                    )
                )
            )
            ret.append(  # fallback info
                Elem(text=PlainText(str="[闪照]请使用新版手机QQ查看".encode()))
            )
        elif isinstance(e, models.AtElement):
            ret.append(
                Elem(
                    text=PlainText(
                        str=e.display.encode(),
                        attr_6_buf=b"\x00\x01\x00\x00\x00\x03\x00"+e.target.to_bytes(4, "big", signed=False)+b"\x00\x00"
                    )
                )
            )
        elif isinstance(e, models.RichMsgElement):
            if len(e.content) > 256:  # compress require
                content = b"\x01" + zlib.compress(e.content, level=6)
            else:
                content = b"\x00" + e.content
            if e.service_id == -2:  # LightApp
                ret_elem = Elem(light_app=LightAppElem(
                    data=content
                ))
            else:  # Json & Xml
                ret_elem = Elem(rich_msg=RichMsg(
                    template_1=content,
                    service_id=0 if e.service_id < 0 else e.service_id
                ))
            ret.append(ret_elem)
        else:
            raise NotImplementedError(e)

    return MsgBody(
        rich_text=RichText(
            elems=ret,
            ptt=None
        )
    )


def encode_send_group_msg_req(
    seq: int, group: int, body: MsgBody, head: ContentHead
) -> PbSendMsgReq:
    return PbSendMsgReq(
        routing_head=RoutingHead(grp=Grp(group_code=group)),
        content_head=head,
        body=body,
        seq=seq,
        rand=random.randrange(300000, 3000000),
        via=1,
    )


def make_group_msg_pkg(seq: int, gid: int, body: MsgBody) -> PbSendMsgReq:
    return encode_send_group_msg_req(
        seq, gid, body, ContentHead(pkg_num=1, pkg_index=0, div_seq=0)
    )
