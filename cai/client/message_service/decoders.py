"""MessageSvc message decoder.

This module is used to decode message protobuf.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
from itertools import chain
from typing import Dict, List, Callable, Optional

from cai.log import logger
from cai.pb.msf.msg.comm import Msg
from cai.client.message import parse_ptt, parse_elements
from cai.client.events import Event, GroupMessageEvent, PrivateMessageEvent


class BuddyMessageDecoder:
    """Buddy Message Decoder.

    Note:
        Source:
        com.tencent.mobileqq.service.message.codec.decoder.buddyMessage.BuddyMessageDecoder
    """

    @classmethod
    def decode(cls, message: Msg) -> Optional[Event]:
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
        Decoder = sub_decoders.get(message.head.c2c_cmd)
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
        parsed_elems = []
        if message.body.rich_text.HasField("ptt"):
            parsed_elems.append(parse_ptt(message.body.rich_text.ptt))
        parsed_elems.extend(parse_elements(message.body.rich_text.elems))

        return PrivateMessageEvent(
            _msg=message,
            seq=seq,
            time=time,
            auto_reply=auto_reply,
            user_id=from_uin,
            user_nick=from_nick,
            to_id=to_uin,
            message=parsed_elems,
        )


class TroopMessageDecoder:
    """Troop Message Decoder(Processor).

    Note:
        Source: com.tencent.mobileqq.troop.data.TroopMessageProcessor
    """

    __slots__ = ()

    long_msg_fragment_store: Dict[int, List[Msg]] = {}

    @classmethod
    def decode(cls, message: Msg) -> Optional[Event]:
        """Troop Message Processor.

        Note:
            Source:

            com.tencent.mobileqq.troop.data.TroopMessageProcessor.a

            com.tencent.imcore.message.BaseMessageProcessorForTroopAndDisc.a
        """
        if not message.head.HasField("group_info"):
            return

        seq = message.head.seq
        time = message.head.time
        from_uin = message.head.from_uin
        troop = message.head.group_info
        content_head = message.content_head
        parsed_elems = []
        ptts = (
            [message.body.rich_text.ptt]
            if message.body.rich_text.HasField("ptt")
            else []
        )
        elems = message.body.rich_text.elems

        # long msg fragment
        if content_head.pkg_num > 1:
            fragments = cls.long_msg_fragment_store.setdefault(
                content_head.div_seq, []
            )
            fragments.append(message)
            if len(fragments) < content_head.pkg_num:
                return

            cls.long_msg_fragment_store.pop(content_head.div_seq)
            f = sorted(fragments, key=lambda f: f.content_head.pkg_index)
            ptts = [
                msg.body.rich_text.ptt
                for msg in f
                if msg.body.rich_text.HasField("ptt")
            ]
            elems = list(
                chain.from_iterable(msg.body.rich_text.elems for msg in f)
            )

        parsed_elems.extend(map(parse_ptt, ptts))
        parsed_elems.extend(parse_elements(elems))

        return GroupMessageEvent(
            _msg=message,
            seq=seq,
            time=time,
            group_id=troop.group_code,
            group_name=troop.group_name.decode("utf-8"),
            group_level=troop.group_level,
            from_uin=from_uin,
            from_group_card=troop.group_card.decode("utf-8"),
            message=parsed_elems,
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
