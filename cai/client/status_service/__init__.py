"""StatSvc Related SDK.

This module is used to build and handle status service related packet.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""

from jce import types
from typing import TYPE_CHECKING

from .jce import SvcReqRegister
from cai.utils.binary import Packet
from cai.settings.device import get_device
from cai.settings.protocol import get_protocol
from cai.utils.jce import RequestPacketVersion3
from cai.pb.oicq.cmd0x769_pb2 import ConfigSeq, ReqBody
from .event import SvcRegisterResponse, RegisterSuccess, RegisterFail
from cai.client.packet import CSsoBodyPacket, CSsoDataPacket, IncomingPacket

if TYPE_CHECKING:
    from cai.client import Client

DEVICE = get_device()
APK_INFO = get_protocol()


# register
def encode_register(
    seq: int, session_id: bytes, ksid: bytes, uin: int, tgt: bytes, d2: bytes,
    d2key: bytes
) -> Packet:
    """Build status service register packet.

    Called in `com.tencent.mobileqq.msf.core.push.e.a`.

    command name: `StatSvc.register`

    Note:
        Source: com.tencent.mobileqq.msf.core.push.e.a

    Args:
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        tgt (bytes): siginfo tgt.
        d2 (bytes): siginfo d2.
        d2key (bytes): siginfo d2 key.

    Returns:
        Packet: Register packet.
    """
    COMMAND_NAME = "StatSvc.register"
    SUB_APP_ID = APK_INFO.sub_app_id

    svc = SvcReqRegister(
        uin=uin,
        bid=7,  # login: 1 | 2 | 4, logout: 0
        status=11,  # login: 11, logout: 21
        ios_version=DEVICE.version.sdk,
        nettype=bytes([1]),
        reg_type=bytes(1),
        guid=DEVICE.guid,
        dev_name=DEVICE.model,
        dev_type=DEVICE.model,
        os_version=DEVICE.version.release,
        large_seq=0,
        vendor_name=DEVICE.vendor_name,
        vendor_os_name=DEVICE.vendor_os_name,
        b769_req=ReqBody(
            config_list=[
                ConfigSeq(type=46, version=0),
                ConfigSeq(type=283, version=0)
            ]
        ).SerializeToString(),
        is_set_status=False,
        set_mute=False,
        ext_online_status=1000,
        battery_status=98
    )
    payload = SvcReqRegister.to_bytes(0, svc)
    req_packet = RequestPacketVersion3(
        servant_name="PushService",
        func_name="SvcReqRegister",
        data=types.MAP({types.STRING("SvcReqRegister"): types.BYTES(payload)})
    ).encode()
    sso_packet = CSsoBodyPacket.build(
        seq,
        SUB_APP_ID,
        COMMAND_NAME,
        DEVICE.imei,
        session_id,
        ksid,
        body=req_packet,
        extra_data=tgt
    )
    packet = CSsoDataPacket.build(uin, 1, sso_packet, key=d2key, extra_data=d2)
    return packet


def decode_register_response(
    client: "Client", packet: IncomingPacket
) -> SvcRegisterResponse:
    return SvcRegisterResponse.decode_response(
        packet.uin, packet.seq, packet.ret_code, packet.command_name,
        packet.data
    )


__all__ = [
    "encode_register", "decode_register_response", "SvcRegisterResponse",
    "RegisterSuccess", "RegisterFail"
]
