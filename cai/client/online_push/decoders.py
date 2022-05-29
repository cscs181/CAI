import re
import json
from typing import Any, Dict, List, Tuple, Callable, Iterator

from cai.log import logger
from cai.client.events import Event
from cai.utils.binary import Packet
from cai.pb.im.oidb.cmd0x857.troop_tips import NotifyMsgBody
from cai.client.events.group import (
    GroupNudgeEvent,
    GroupRedbagEvent,
    GroupMemberMutedEvent,
    GroupNameChangedEvent,
    GroupMemberUnMutedEvent,
    GroupMessageRecalledEvent,
    GroupLuckyCharacterNewEvent,
    GroupLuckyCharacterInitEvent,
    GroupLuckyCharacterClosedEvent,
    GroupLuckyCharacterOpenedEvent,
    GroupLuckyCharacterChangedEvent,
    GroupMemberSpecialTitleChangedEvent,
)

from .jce import MessageInfo

DT = Callable[[MessageInfo], Iterator[Event]]


def parse_cmds(content: str) -> Tuple[str, List[Dict[str, Any]]]:
    cmds: List[Dict[str, Any]] = []
    texts: List[str] = []
    text_begin = 0
    for cmd in re.finditer(r"<([^>]+)>", content):
        texts.append(content[text_begin : cmd.pos + cmd.start()])
        text_begin = cmd.pos + cmd.end()
        cmd_obj = json.loads(cmd.group(1))
        cmd_obj["start_index"] = cmd.pos + cmd.start()
        cmd_obj["end_index"] = cmd.pos + cmd.end()
        cmds.append(cmd_obj)
        if "text" in cmd_obj:
            texts.append(cmd_obj["text"])
    texts.append(content[text_begin:])
    return "".join(texts), cmds


class GroupEventDecoder:
    """Group Event Decoder.

    Note:
        Source:
        com.tencent.imcore.message.OnLinePushMessageProcessor.ProcessOneMsg.a
    """

    __slots__ = ()

    @classmethod
    def decode(cls, info: MessageInfo) -> Iterator[Event]:
        content = info.vec_msg
        sub_type = content[4]

        sub_decoders: Dict[int, DT] = {
            # 6: cls.decode_troop_exit,  # troop exit message
            # 11: cls.decode_group_visitor_join,  # group visitor join tencent.im.group.cmd0x2dc
            12: cls.decode_troop_gag,
            # 13: cls.decode_group_visitor_join,
            14: cls.decode_troop_gag,
            # 15: cls.decode_troop,  # troop manager
            16: cls.decode_troop_tips,
            17: cls.decode_troop_tips,
            20: cls.decode_troop_tips,
            21: cls.decode_troop_tips,
        }
        Decoder = sub_decoders.get(sub_type, None)
        if not Decoder:
            logger.debug(
                "OnlinePush.ReqPush: GroupEventDecoder cannot "
                f"decode event with subtype {sub_type}"
            )
            return
        yield from Decoder(info)

    @classmethod
    def decode_troop_gag(cls, info: MessageInfo) -> Iterator[Event]:
        """Troop Gag Manager.

        Sub Type: 12, 14

        Note:
            Source: com.tencent.mobileqq.troop.utils.TroopGagMgr.a
        """
        data = Packet(info.vec_msg)
        group_id, sub_type = data.start().uint32().uint8().execute()
        if sub_type == 12:
            operator_id, count = (
                data.start().offset(6).uint32().offset(4).uint16().execute()
            )

            offset = 16
            for _ in range(count):
                target_id, duration = (
                    data.start().offset(offset).uint32().uint32().execute()
                )
                offset += 8
                if duration > 0:
                    yield GroupMemberMutedEvent(
                        group_id=group_id,
                        operator_id=operator_id,
                        target_id=target_id,
                        duration=duration,
                    )
                else:
                    yield GroupMemberUnMutedEvent(
                        group_id=group_id,
                        operator_id=operator_id,
                        target_id=target_id,
                    )
        # elif sub_type == 14:

    @classmethod
    def decode_troop_tips(cls, info: MessageInfo) -> Iterator[Event]:
        """Troop Tips Message Manager.

        Sub Type: 16, 17, 20, 21

        Prompt Type:
            1: red/gray tip
            2: ignore
            3: ignore
            4: ignore
            5: ignore
            6: troop feeds
            7: message recall
            8: ignore
            9: notify obj msg update push
            10: 0x857 werewolf push
            11: 0x857 game status notify
            12: apollo msg
            13: gold msg tips
            14: ignore
            15: miniapp notify -> group open sys msg
            16: ignore
            17: recv msg set changed
            18: prompt troop form tips
            19: msg media push
            20: general gray tip
            21: msg video push
            22: troop location push
            23: msg sing push
            24: group info change
            25: group announce tbc info
            26: qq video game push
            27: group digest msg
            28: ignore
            29: ignore
            30: qq live notify
            31: group digest msg summary
            32: revert gray tips traceless

        Note:
            Source: com.tencent.mobileqq.troop.utils.TroopTipsMsgMgr.a
        """
        content = info.vec_msg
        if len(content) <= 7:
            return
        tip = NotifyMsgBody.FromString(content[7:])
        prompt_type = tip.enum_type
        group_id = tip.group_code
        service_type = tip.service_type
        if prompt_type == 1:
            if tip.HasField("redtips"):
                # FIXME: more detailed events
                yield GroupRedbagEvent(
                    group_id=group_id, sender_id=tip.redtips.sender_uin
                )
            if tip.HasField("graytips"):
                content = tip.graytips.content.decode("utf-8")
                if content:
                    text, cmds = parse_cmds(content)
                    if service_type == 6:
                        yield GroupMemberSpecialTitleChangedEvent(
                            group_id=group_id,
                            text=text,
                            raw_text=content,
                            cmds=cmds,
                            user_id=tip.graytips.receiver_uin,
                        )
                    elif service_type == 11:
                        # Unknown
                        pass
                    elif service_type == 12:
                        yield GroupNameChangedEvent(
                            group_id=group_id,
                            text=text,
                            raw_text=content,
                            cmds=cmds,
                        )
                    else:
                        logger.debug(
                            f"Unknown service type: {service_type}, content: {content}"
                        )
        elif prompt_type == 7:
            if tip.HasField("recall"):
                msg_list = tip.recall.recalled_msg_list
                for msg in msg_list:
                    yield GroupMessageRecalledEvent(
                        group_id=group_id,
                        operator_id=tip.recall.uin,
                        author_id=msg.author_uin,
                        msg_seq=msg.seq,
                        msg_time=msg.time,
                        msg_type=msg.msg_type,
                        msg_random=msg.msg_random,
                        is_anony_msg=bool(msg.is_anony_msg),
                    )
        elif prompt_type == 20:
            if tip.HasField("general_gray_tip"):
                graytip = tip.general_gray_tip
                busi_type = graytip.busi_type
                busi_id = graytip.busi_id
                if busi_type == 12 and busi_id == 1061:
                    # com.tencent.mobileqq.activity.aio.avatardoubletap.PaiYiPaiMsgUtil
                    yield GroupNudgeEvent(
                        group_id=group_id,
                        template_id=graytip.templ_id,
                        template_text=graytip.content.decode("utf-8"),
                        template_params=dict(
                            (p.name.decode("utf-8"), p.value.decode("utf-8"))
                            for p in graytip.templ_param
                        ),
                    )
                # elif busi_type == 12 and busi_id == 1062:
                #    # 动作，效果
                elif busi_id == 1069:  # busi_type == 1
                    yield GroupLuckyCharacterInitEvent(
                        group_id=group_id,
                        template_id=graytip.templ_id,
                        template_text=graytip.content.decode("utf-8"),
                        template_params=dict(
                            (p.name.decode("utf-8"), p.value.decode("utf-8"))
                            for p in graytip.templ_param
                        ),
                    )
                elif busi_id == 1070:
                    yield GroupLuckyCharacterNewEvent(
                        group_id=group_id,
                        template_id=graytip.templ_id,
                        template_text=graytip.content.decode("utf-8"),
                        template_params=dict(
                            (p.name.decode("utf-8"), p.value.decode("utf-8"))
                            for p in graytip.templ_param
                        ),
                    )
                elif busi_id == 1071:
                    yield GroupLuckyCharacterChangedEvent(
                        group_id=group_id,
                        template_id=graytip.templ_id,
                        template_text=graytip.content.decode("utf-8"),
                        template_params=dict(
                            (p.name.decode("utf-8"), p.value.decode("utf-8"))
                            for p in graytip.templ_param
                        ),
                    )
                elif busi_id == 1072:
                    yield GroupLuckyCharacterClosedEvent(
                        group_id=group_id,
                        template_id=graytip.templ_id,
                        template_text=graytip.content.decode("utf-8"),
                        template_params=dict(
                            (p.name.decode("utf-8"), p.value.decode("utf-8"))
                            for p in graytip.templ_param
                        ),
                    )
                elif busi_id == 1073:
                    yield GroupLuckyCharacterOpenedEvent(
                        group_id=group_id,
                        template_id=graytip.templ_id,
                        template_text=graytip.content.decode("utf-8"),
                        template_params=dict(
                            (p.name.decode("utf-8"), p.value.decode("utf-8"))
                            for p in graytip.templ_param
                        ),
                    )
                # TODO: busi_id 1052, 1053, 1054, 1067 group honor
        elif prompt_type == 24:
            if tip.HasField("group_info_change"):
                ...
        elif prompt_type == 27:
            if tip.HasField("qq_group_digest_msg"):
                ...
        elif prompt_type == 32:
            if tip.HasField("revert_graytips_traceless"):
                ...


ONLINEPUSH_DECODERS: Dict[int, DT] = {
    # 169: handleC2COnlinePushMsgResp,
    # 8: HandleShMsgType0x08
    # 132: HandleShMsgType0x84
    732: GroupEventDecoder.decode
}
"""Online Push ReqPush Decoders.

Note:
    Source: com.tencent.imcore.message.OnLinePushMessageProcessor.ProcessOneMsg.a
"""
