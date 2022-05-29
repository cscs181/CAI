import zlib
from typing import List, Sequence

from cai.pb.im.msg.obj_msg import ObjMsg
from cai.pb.im.msg.msg_body import Ptt, Elem
from cai.pb.im.msg.service.comm_elem import (
    MsgElemInfo_servtype2,
    MsgElemInfo_servtype3,
    MsgElemInfo_servtype33,
)

from .models import *


def parse_elements(elems: Sequence[Elem]) -> List[Element]:
    """Parse message rich text elements.

    Only parse ``text``, ``face``, ``small_smoji``, ``common_elem service 33``
    for plain text.

    Note:
        Source: com.tencent.imcore.message.ext.codec.decoder.pbelement.*

    Args:
        elems (Sequence[Elem]): Sequence of rich text elements.
        ptt (Ptt)

    Returns:
        List[Element]: List of decoded message elements.
    """
    res: List[Element] = []
    index = 0
    while index < len(elems):
        elem = elems[index]
        # SrcElemDecoder
        if elem.HasField("src_msg"):
            if len(elem.src_msg.orig_seqs) > 0:
                # preprocess
                # Delete redundancy data
                # if index == 2:  # Sent by PC
                #     res = []
                # else:
                #     index += 1  # pass
                res.append(
                    ReplyElement(
                        elem.src_msg.orig_seqs[0],
                        elem.src_msg.time,
                        elem.src_msg.sender_uin,
                        parse_elements(elem.src_msg.elems),
                        elem.src_msg.troop_name.decode("utf-8") or None,
                    )
                )
        # TextElemDecoder
        elif elem.HasField("text"):
            if elem.text.attr_6_buf:
                if elem.text.attr_6_buf[6]:  # AtAll
                    res.append(AtAllElement())
                else:
                    res.append(
                        AtElement(
                            int.from_bytes(
                                elem.text.attr_6_buf[7:11], "big", signed=False
                            ),
                            elem.text.str.decode("utf-8"),
                        )
                    )
            else:
                res.append(TextElement(elem.text.str.decode("utf-8")))
        elif elem.HasField("rich_msg"):
            if elem.rich_msg.template_1[0]:
                content = zlib.decompress(elem.rich_msg.template_1[1:])
            else:
                content = elem.rich_msg.template_1[1:]
            return [
                RichMsgElement(
                    content,
                    elem.rich_msg.service_id if content[0] == 60 else -1,
                )
            ]
        elif elem.HasField("light_app"):
            if elem.light_app.data[0]:
                content = zlib.decompress(elem.light_app.data[1:])
            else:
                content = elem.light_app.data[1:]
            return [RichMsgElement(content, -2)]
        # TextElemDecoder
        elif elem.HasField("face"):
            res.append(FaceElement(elem.face.index))
        # TextElemDecoder
        elif elem.HasField("small_emoji"):
            index += 1
            text = elems[index].text.str.decode("utf-8")
            res.append(
                SmallEmojiElement(
                    elem.small_emoji.pack_id_sum,
                    text,
                    # bytes(
                    #     [
                    #         0x1FF
                    #         if elem.small_emoji.image_type & 0xFFFF == 2
                    #         else 0xFF,
                    #         elem.small_emoji.pack_id_sum & 0xFFFF,
                    #         elem.small_emoji.pack_id_sum >> 16 & 0xFF,
                    #         elem.small_emoji.pack_id_sum >> 24,
                    #     ]
                    # ),
                )
            )
        # PictureElemDecoder
        elif elem.HasField("custom_face"):
            if elem.custom_face.md5 and elem.custom_face.orig_url:
                res.append(
                    ImageElement(
                        filename=elem.custom_face.file_path,
                        size=elem.custom_face.size,
                        width=elem.custom_face.width,
                        height=elem.custom_face.height,
                        md5=elem.custom_face.md5,
                        url="https://gchat.qpic.cn" + elem.custom_face.orig_url,
                    )
                )
            elif elem.custom_face.md5:
                res.append(
                    ImageElement(
                        filename=elem.custom_face.file_path,
                        size=elem.custom_face.size,
                        width=elem.custom_face.width,
                        height=elem.custom_face.height,
                        md5=elem.custom_face.md5,
                        url="https://gchat.qpic.cn/gchatpic_new/0/0-0-"
                        + elem.custom_face.md5.decode().upper()
                        + "/0",
                    )
                )
        # PictureElemDecoder
        elif elem.HasField("not_online_image"):
            if elem.not_online_image.orig_url:
                res.append(
                    ImageElement(
                        filename=elem.not_online_image.file_path.decode(
                            "utf-8"
                        ),
                        size=elem.not_online_image.file_len,
                        width=elem.not_online_image.pic_width,
                        height=elem.not_online_image.pic_height,
                        md5=elem.not_online_image.pic_md5,
                        url="https://c2cpicdw.qpic.cn"
                        + elem.not_online_image.orig_url,
                    )
                )
            elif (
                elem.not_online_image.res_id
                or elem.not_online_image.download_path
            ):
                res.append(
                    ImageElement(
                        filename=elem.not_online_image.file_path.decode(
                            "utf-8"
                        ),
                        size=elem.not_online_image.file_len,
                        width=elem.not_online_image.pic_width,
                        height=elem.not_online_image.pic_height,
                        md5=elem.not_online_image.pic_md5,
                        url="https://c2cpicdw.qpic.cn/offpic_new/0/"
                        + (
                            elem.not_online_image.res_id
                            or elem.not_online_image.download_path
                        ).decode("utf-8")
                        + "/0",
                    )
                )
        elif elem.HasField("open_qq_data"):
            res.append(CustomDataElement(data=elem.open_qq_data.car_qq_data))
        elif elem.HasField("common_elem"):
            service_type = elem.common_elem.service_type
            # PokeMsgElemDecoder
            if service_type == 2:
                poke = MsgElemInfo_servtype2.FromString(
                    elem.common_elem.pb_elem
                )
                res = [
                    PokeElement(
                        poke.poke_type
                        if poke.vaspoke_id == 0xFFFFFFFF
                        else poke.vaspoke_id,
                        poke.vaspoke_name.decode("utf-8"),
                        poke.poke_strength,
                        poke.double_hit,
                    )
                ]
                break
            elif service_type == 3:
                flash = MsgElemInfo_servtype3.FromString(
                    elem.common_elem.pb_elem
                )
                if flash.flash_troop_pic:
                    res.append(
                        FlashImageElement(
                            id=flash.flash_troop_pic.file_id,
                            filename=flash.flash_troop_pic.file_path,
                            filetype=flash.flash_troop_pic.file_type,
                            size=flash.flash_troop_pic.size,
                            md5=flash.flash_troop_pic.md5,
                            width=flash.flash_troop_pic.width,
                            height=flash.flash_troop_pic.height,
                            url=f"https://gchat.qpic.cn/gchatpic_new/0/0-0-{flash.flash_troop_pic.md5.hex().upper()}/0",
                        )
                    )
                break
            # TextElemDecoder
            elif service_type == 33:
                info = MsgElemInfo_servtype33.FromString(
                    elem.common_elem.pb_elem
                )
                res.append(FaceElement(info.index))
        elif elem.HasField("shake_window"):
            res.append(
                ShakeElement(
                    stype=elem.shake_window.type, uin=elem.shake_window.uin
                )
            )
        elif elem.HasField("trans_elem_info"):
            if elem.trans_elem_info.elem_type == 24:  # QQ File
                if elem.trans_elem_info.elem_value[0]:
                    obj = ObjMsg.FromString(elem.trans_elem_info.elem_value[3:])
                    for info in obj.content_info:
                        res.append(
                            GroupFileElement(
                                info.file.file_name,
                                info.file.file_size,
                                info.file.file_path.decode(),
                                bytes.fromhex(info.file.file_md5.decode()),
                            )
                        )
        index += 1
    return res


def parse_ptt(ptt: Ptt) -> VoiceElement:
    """Parse message ptt elements.

    Note:
        Source: com.tencent.mobileqq.service.message.codec.decoder.PTTDecoder

    Args:
        ptt (Ptt): ptt element in msg

    Returns:
        VoiceElement: Parsed VoiceElement object.
    """
    return VoiceElement(
        file_name=ptt.file_name.decode(),
        file_type=ptt.file_type,
        file_size=ptt.file_size,
        file_uuid=ptt.file_uuid,
        file_md5=ptt.file_md5,
        url=ptt.down_para.decode(),
    )
