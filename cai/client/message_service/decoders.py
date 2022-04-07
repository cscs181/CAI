"""MessageSvc message decoder.

This module is used to decode message protobuf.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import zlib
from itertools import chain
from typing import Dict, List, Callable, Optional, Sequence

from cai.log import logger
from cai.client.events.base import Event
from cai.pb.msf.msg.comm import Msg
from cai.pb.im.msg.msg_body import Ptt, Elem
from cai.pb.im.msg.service.comm_elem import (
    MsgElemInfo_servtype2,
    MsgElemInfo_servtype3,
    MsgElemInfo_servtype33,
)

from .models import (
    Element,
    AtElement,
    FaceElement,
    PokeElement,
    TextElement,
    AtAllElement,
    GroupMessage,
    ImageElement,
    ReplyElement,
    ShakeElement,
    VoiceElement,
    PrivateMessage,
    RichMsgElement,
    FlashImageElement,
    SmallEmojiElement,
)


def parse_elements(elems: Sequence[Elem], ptt: Optional[Ptt]) -> List[Element]:
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
    if ptt:
        if ptt.file_name.endswith(b".amr"):
            info = {}
            for bl in ptt.down_para.decode().split("&")[1:]:
                k, v = bl.split("=", 1)
                info[k] = v
            return [
                VoiceElement(
                    ptt.file_name.decode(),
                    info["filetype"],
                    ptt.src_uin,
                    ptt.file_md5,
                    ptt.file_size,
                    bytes.fromhex(info["rkey"]),
                    "https://grouptalk.c2c.qq.com" + ptt.down_para.decode(),
                )
            ]
    res: List[Element] = []
    index = 0
    while index < len(elems):
        elem = elems[index]
        # SrcElemDecoder
        if elem.HasField("src_msg"):
            if len(elem.src_msg.orig_seqs) > 0:
                # preprocess
                # Delete redundancy data
                if index == 2:  # Sent by PC
                    res = []
                else:
                    index += 1  # pass
                res.append(
                    ReplyElement(
                        elem.src_msg.orig_seqs[0],
                        elem.src_msg.time,
                        elem.src_msg.sender_uin,
                        parse_elements(elem.src_msg.elems, None),
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
        index += 1
    return res


class BuddyMessageDecoder:
    @classmethod
    def decode(cls, message: Msg) -> Optional[Event]:
        """Buddy Message Decoder.

        Note:
            Source:
            com.tencent.mobileqq.service.message.codec.decoder.buddyMessage.BuddyMessageDecoder
        """
        sub_decoders: Dict[int, Callable[[Msg], Optional[Event]]] = {
            11: cls.decode_normal_buddy,
            # 129: OnlineFileDecoder,
            # 131: OnlineFileDecoder,
            # 133: OnlineFileDecoder,
            # 169: OfflineFileDecoder,
            175: cls.decode_normal_buddy,
            # 241: OfflineFileDecoder,
            # 242: OfflineFileDecoder,
            # 243: OfflineFileDecoder,
        }
        Decoder = sub_decoders.get(message.head.c2c_cmd, None)
        if not Decoder:
            logger.debug(
                "MessageSvc.PbGetMsg: BuddyMessageDecoder cannot "
                f"decode message with c2c_cmd {message.head.c2c_cmd}"
            )
            return
        return Decoder(message)

    @classmethod
    def decode_normal_buddy(cls, message: Msg) -> Optional[Event]:
        """Normal Buddy Message Decoder.

        Note:
            Source:

            com.tencent.mobileqq.service.message.codec.decoder.buddyMessage.NormalBuddyDecoder

            com.tencent.mobileqq.service.message.MessagePBElemDecoder
        """
        if (
            not message.HasField("body")
            or not message.body.HasField("rich_text")
            or not message.body.rich_text.elems
            or not message.HasField("content_head")
        ):
            return

        seq = message.head.seq
        time = message.head.time
        auto_reply = bool(message.content_head.auto_reply)
        from_uin = message.head.from_uin
        from_nick = message.head.from_nick
        to_uin = message.head.to_uin
        elems = message.body.rich_text.elems
        ptt = message.body.rich_text.ptt

        return PrivateMessage(
            message,
            seq,
            time,
            auto_reply,
            from_uin,
            from_nick,
            to_uin,
            parse_elements(elems, ptt),
        )


class TroopMessageDecoder:
    long_msg_fragment_store: Dict[int, List[Msg]] = {}

    @classmethod
    def decode(cls, message: Msg) -> Optional[Event]:
        if not message.head.HasField("group_info"):
            return

        seq = message.head.seq
        time = message.head.time
        from_uin = message.head.from_uin
        troop = message.head.group_info
        content_head = message.content_head
        elems = message.body.rich_text.elems
        ptt = message.body.rich_text.ptt

        # long msg fragment
        if content_head.pkg_num > 1:
            fragments = cls.long_msg_fragment_store.setdefault(
                content_head.div_seq, []
            )
            fragments.append(message)
            if len(fragments) < content_head.pkg_num:
                return

            cls.long_msg_fragment_store.pop(content_head.div_seq)
            elems = list(
                chain.from_iterable(
                    msg.body.rich_text.elems
                    for msg in sorted(
                        fragments, key=lambda f: f.content_head.pkg_index
                    )
                )
            )

        return GroupMessage(
            message,
            seq,
            time,
            troop.group_code,
            troop.group_name.decode("utf-8"),
            troop.group_level,
            from_uin,
            troop.group_card.decode("utf-8"),
            parse_elements(elems, ptt),
        )


class TempSessionDecoder:
    @classmethod
    def decode(cls, message: Msg) -> Optional[Event]:
        # TODO
        ...


MESSAGE_DECODERS: Dict[int, Callable[[Msg], Optional[Event]]] = {
    9: BuddyMessageDecoder.decode,
    10: BuddyMessageDecoder.decode,
    31: BuddyMessageDecoder.decode,
    # 33: TroopAddMemberBroadcastDecoder,
    # 35: TroopSystemMessageDecoder,
    # 36: TroopSystemMessageDecoder,
    # 37: TroopSystemMessageDecoder,
    # 38: CreateGrpInPCDecoder,
    43: TroopMessageDecoder.decode,
    # 45: TroopSystemMessageDecoder,
    # 46: TroopSystemMessageDecoder,
    82: TroopMessageDecoder.decode,
    # 84: TroopSystemMessageDecoder,
    # 85: TroopSystemMessageDecoder,
    # 86: TroopSystemMessageDecoder,
    # 87: TroopSystemMessageDecoder,
    79: BuddyMessageDecoder.decode,
    97: BuddyMessageDecoder.decode,
    120: BuddyMessageDecoder.decode,
    132: BuddyMessageDecoder.decode,
    133: BuddyMessageDecoder.decode,
    140: TempSessionDecoder.decode,
    141: TempSessionDecoder.decode,
    166: BuddyMessageDecoder.decode,
    167: BuddyMessageDecoder.decode,
    # 187: SystemMessageDecoder,
    # 188: SystemMessageDecoder,
    # 189: SystemMessageDecoder,
    # 190: SystemMessageDecoder,
    # 191: SystemMessageDecoder,
    # 193: VideoDecoder,
    # 208: PTTDecoder,
    # 519: MultiVideoDecoder,
    # 524: DiscussionUpdateDecoder,
    # 528: MsgType0x210Decoder,
    # 529: MsgType0x211Decoder,
    # 562: VideoQCallDecoder,
    # 732: MsgType0x2dcDecoder,
    # 734: SharpVideoDecoder,
}
"""C2C Message Decoders.

Note:
    Source: com.tencent.mobileqq.app.QQMessageFacadeConfig.start
"""
