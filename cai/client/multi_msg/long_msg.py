from cai.client import Command
from cai.pb.highway.longmsg.longmsg_pb2 import MultiReqBody, MultiMsgApplyUpReq, MultiMsgApplyUpRsp, MultiRspBody
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
    data: MultiRspBody


async def build_multi_apply_up_pkg(client: "Client", group_id: int, data_len: int, data_md5: bytes, bu_type: int):
    body: MultiApplyResp = await client.send_unipkg_and_wait(
        client.next_seq(),
        "MultiMsg.ApplyUp",
        _encode_multi_req_body(
            group_id, data_len, data_md5, bu_type
        ).SerializeToString()
    )
    





async def handle_multi_resp_body(client: "Client", pkg: "IncomingPacket", _device) -> MultiApplyResp:
    return MultiApplyResp(
        uin=pkg.uin,
        seq=pkg.seq,
        ret_code=pkg.ret_code,
        command_name=pkg.command_name,
        data=MultiRspBody.FromString(pkg.data)
    )
