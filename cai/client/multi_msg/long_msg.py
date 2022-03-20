from cai.client import Command
from cai.pb.highway.multi_msg.multi_msg_pb2 import MultiReqBody, MultiMsgApplyUpReq, MultiMsgApplyUpRsp, MultiRspBody
from cai.pb.highway.long_msg.long_msg_pb2 import LongReqBody, LongMsgUpReq
from typing import TYPE_CHECKING

from dataclasses import dataclass

if TYPE_CHECKING:
    from cai.client.packet import IncomingPacket
    from cai.client.client import Client


def _encode_multi_req_body(group_id: int, data_len: int, data_md5: bytes, bu_type: int) -> MultiReqBody:
    return MultiReqBody(
        subcmd=1,
        termType=5,
        platformType=9,
        netType=3,
        buildVer="8.2.0.1297",  # modify
        multimsgApplyupReq=[MultiMsgApplyUpReq(
            dstUin=group_id,
            msgSize=data_len,
            msgMd5=data_md5,
            msgType=3
        )],
        buType=bu_type
    )


@dataclass
class MultiApplyResp(Command):
    data: MultiMsgApplyUpRsp


async def build_multi_apply_up_pkg(client: "Client", group_id: int, data_len: int, data_md5: bytes, bu_type: int):
    body: MultiApplyResp = await client.send_unipkg_and_wait(
        client.next_seq(),
        "MultiMsg.ApplyUp",
        _encode_multi_req_body(
            group_id, data_len, data_md5, bu_type
        ).SerializeToString()
    )
    LongReqBody(
        subcmd=1,
        termType=5,
        platformType=9,
        msgUpReq=[LongMsgUpReq(
            msgType=3,
            dstUin=client.uin,
            msgContent=bytes(),  # todo:
            storeType=2,
            msgUkey=body.data.msgUkey
        )]
    )





async def _handle_multi_resp_body(client: "Client", pkg: "IncomingPacket", _device) -> MultiApplyResp:
    mrb = MultiRspBody.FromString(pkg.data).multimsgApplyupRsp
    if not mrb:
        raise ConnectionError("no MultiMsgApplyUpRsp Found")
    return MultiApplyResp(
        uin=pkg.uin,
        seq=pkg.seq,
        ret_code=pkg.ret_code,
        command_name=pkg.command_name,
        data=mrb[0]
    )
