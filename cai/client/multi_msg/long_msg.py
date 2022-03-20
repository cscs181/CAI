from cai.client import Command
from cai.pb.highway.longmsg.longmsg_pb2 import MultiReqBody, MultiMsgApplyUpReq, MultiMsgApplyUpRsp
from typing import TYPE_CHECKING

from dataclasses import dataclass

if TYPE_CHECKING:
    from cai.client.packet import IncomingPacket
    from cai.client.client import Client


def encode_multi_apply_up_pkg(group_id: int, data_len: int, data_md5: bytes, bu_type: int) -> bytes:
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
    ).SerializeToString()


@dataclass
class MultiApplyUpResp(Command):
    data: MultiMsgApplyUpRsp


async def handle_multi_apply_up_resp(client: "Client", pkg: "IncomingPacket", _device):
    return MultiApplyUpResp(
        uin=pkg.uin,
        seq=pkg.seq,
        ret_code=pkg.ret_code,
        command_name=pkg.command_name,
        data=MultiMsgApplyUpRsp.FromString(pkg.data)
    )
