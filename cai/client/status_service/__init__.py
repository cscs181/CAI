"""StatSvc Related SDK.

This module is used to build and handle status service related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

import time
from enum import Enum, IntEnum
from typing import TYPE_CHECKING, Tuple, Union, Optional

from jce import types

from cai.log import logger
from cai.utils.binary import Packet
from cai.settings.protocol import ApkInfo
from cai.settings.device import DeviceInfo
from cai.utils.jce import RequestPacketVersion3
from cai.pb.im.oidb.cmd0x769 import ReqBody, ConfigSeq
from cai.client.packet import (
    UniPacket,
    CSsoBodyPacket,
    CSsoDataPacket,
    IncomingPacket,
)

from .jce import SvcReqRegister, ResponseMSFForceOffline
from .command import (
    RegisterFail,
    MSFForceOffline,
    RegisterSuccess,
    SvcRegisterResponse,
    MSFForceOfflineError,
    MSFForceOfflineCommand,
)

if TYPE_CHECKING:
    from cai.client import Client


class OnlineStatus(IntEnum):
    """
    Note:
        Source: mqq.app.AppRuntime
    """

    Unknown = 0
    """未知"""
    Online = 11
    """我在线上"""
    Offline = 21
    """离线"""
    Away = 31
    """离开"""
    Invisible = 41
    """隐身"""
    Busy = 50
    """忙碌"""
    Qme = 60
    """Q 我吧"""
    Dnd = 70
    """请勿打扰"""
    ReceiveOfflineMsg = 95
    """离线但接收消息"""
    Battery = 1000
    """当前电量"""
    Listening = 1028
    """听歌中"""
    Constellation = 1040
    """星座运势"""
    Weather = 1030
    """今日天气"""
    MeetSpring = 1069
    """遇见春天"""
    Timi = 1027
    """Timi中"""
    EatChicken = 1064
    """吃鸡中"""
    Loving = 1051
    """恋爱中"""
    WangWang = 1053
    """汪汪汪"""
    CookedRice = 1019
    """干饭中"""
    Study = 1018
    """学习中"""
    StayUp = 1032
    """熬夜中"""
    PlayBall = 1050
    """打球中"""
    Signal = 1011
    """信号弱"""
    StudyOnline = 1024
    """在线学习"""
    Gaming = 1017
    """游戏中"""
    Vacationing = 1022
    """度假中"""
    WatchingTV = 1021
    """追剧中"""
    Fitness = 1020
    """健身中"""

    @classmethod
    def _missing_(cls, value: int) -> "OnlineStatus":
        return OnlineStatus.Unknown


class RegPushReason(str, Enum):
    """
    Note:
        Source: com.tencent.mobileqq.msf.core.push.RegPushReason
    """

    MsfBoot = "msfBoot"
    AppRegister = "appRegister"
    Unknown = "unknown"
    MsfHeartTimeTooLong = "msfHeartTimeTooLong"
    MsfByNetChange = "msfByNetChange"
    ServerPush = "serverPush"
    FillRegProxy = "fillRegProxy"
    CreateDefaultRegInfo = "createDefaultRegInfo"
    SetOnlineStatus = "setOnlineStatus"


def _encode_svc_request(
    uin: int,
    status: Union[int, OnlineStatus],
    reg_push_reason: Union[str, RegPushReason],
    device: DeviceInfo,
    battery_status: Optional[int] = None,
    is_power_connected: bool = False,
) -> SvcReqRegister:
    assert (
        battery_status is None or 0 <= battery_status <= 100
    ), "Battery Capacity Error!"

    return SvcReqRegister(
        uin=uin,
        bid=0 if status == OnlineStatus.Offline else 7,
        status=status if status < 1000 else OnlineStatus.Online,
        timestamp=int(time.time()),
        ios_version=device.version.sdk,
        nettype=bytes([1]),
        reg_type=bytes(1)
        if reg_push_reason
        in (
            RegPushReason.AppRegister,
            RegPushReason.FillRegProxy,
            RegPushReason.CreateDefaultRegInfo,
            RegPushReason.SetOnlineStatus,
        )
        else bytes([1]),
        guid=device.guid,
        dev_name=device.model,
        dev_type=device.model,
        os_version=device.version.release,
        large_seq=0,
        vendor_name=device.vendor_name,
        vendor_os_name=device.vendor_os_name,
        b769_req=ReqBody(
            config_list=[
                ConfigSeq(type=46, version=0),
                ConfigSeq(type=283, version=0),
            ]
        ).SerializeToString(),
        is_set_status=reg_push_reason == RegPushReason.SetOnlineStatus,
        set_mute=False,
        ext_online_status=status if status >= 1000 else 0,
        battery_status=(battery_status or 0) | (128 * is_power_connected),
    )


# register
def encode_register(
    seq: int,
    session_id: bytes,
    ksid: bytes,
    uin: int,
    tgt: bytes,
    d2: bytes,
    d2key: bytes,
    status: Union[int, OnlineStatus],
    reg_push_reason: Union[str, RegPushReason],
    sub_app_id: int,
    device: DeviceInfo,
) -> Packet:
    """Build status service register packet.

    Called in ``com.tencent.mobileqq.msf.core.push.e.a``.

    command name: ``StatSvc.register``

    Note:
        Source: com.tencent.mobileqq.msf.core.push.e.a

    Args:
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        tgt (bytes): Siginfo tgt.
        d2 (bytes): Siginfo d2.
        d2key (bytes): Siginfo d2 key.
        status (Union[int, OnlineStatus]): Online status.
        reg_push_reason (Union[str, RegPushReason]): Reg push reason.
        device (DeviceInfo): your device info
        sub_app_id (int): ApkInfo

    Returns:
        Packet: Register packet.
    """
    COMMAND_NAME = "StatSvc.register"
    SUB_APP_ID = sub_app_id

    svc = _encode_svc_request(uin, status, reg_push_reason, device)
    payload = SvcReqRegister.to_bytes(0, svc)
    req_packet = RequestPacketVersion3(
        servant_name="PushService",
        func_name="SvcReqRegister",
        data=types.MAP({types.STRING("SvcReqRegister"): types.BYTES(payload)}),
    ).encode()
    sso_packet = CSsoBodyPacket.build(
        seq,
        SUB_APP_ID,
        COMMAND_NAME,
        device.imei,
        session_id,
        ksid,
        body=req_packet,
        extra_data=tgt,
    )
    packet = CSsoDataPacket.build(uin, 1, sso_packet, key=d2key, extra_data=d2)
    return packet


# set status from client
def encode_set_status(
    seq: int,
    session_id: bytes,
    uin: int,
    d2key: bytes,
    device: DeviceInfo,
    status: Union[int, OnlineStatus],
    battery_status: Optional[int] = None,
    is_power_connected: bool = False,
) -> Packet:
    """Build status service register packet.

    Called in ``com.tencent.mobileqq.msf.core.push.e.a``.

    command name: ``StatSvc.SetStatusFromClient``

    Note:
        Source: com.tencent.mobileqq.msf.core.push.e.a

    Args:
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        uin (int): User QQ number.
        d2key (bytes): Siginfo d2 key.
        status (Union[int, OnlineStatus]): Online status.
        device (DeviceInfo): your device info
        battery_status (Optional[int], optional): Battery capacity.
            Only works when status is :obj:`.OnlineStatus.Battery`. Defaults to None.
        is_power_connected (bool, optional): Is power connected to phone.
            Only works when status is :obj:`.OnlineStatus.Battery`. Defaults to False.

    Returns:
        Packet: Register packet.
    """
    COMMAND_NAME = "StatSvc.SetStatusFromClient"

    svc = _encode_svc_request(
        uin,
        status,
        RegPushReason.SetOnlineStatus,
        device,
        ((status == OnlineStatus.Battery) or None) and battery_status,
        (status == OnlineStatus.Battery) and is_power_connected,
    )
    payload = SvcReqRegister.to_bytes(0, svc)
    req_packet = RequestPacketVersion3(
        servant_name="PushService",
        func_name="SvcReqRegister",
        data=types.MAP({types.STRING("SvcReqRegister"): types.BYTES(payload)}),
    ).encode()
    packet = UniPacket.build(
        uin, seq, COMMAND_NAME, session_id, 1, req_packet, d2key
    )
    return packet


async def handle_register_response(
    client: "Client", packet: IncomingPacket, _device
) -> SvcRegisterResponse:
    response = SvcRegisterResponse.decode_response(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
    )
    if isinstance(response, RegisterSuccess):
        client._heartbeat_interval = response.response.hello_interval
        client._status = OnlineStatus(
            response.response.ext_online_status
        ) or OnlineStatus(response.response.status)
    return response


def encode_force_offline_response(
    seq: int,
    session_id: bytes,
    ksid: bytes,
    uin: int,
    tgt: bytes,
    d2: bytes,
    d2key: bytes,
    req_uin: int,
    seq_no: int,
    sub_app_id: int,
    device: DeviceInfo,
) -> Packet:
    """Build status service msf offline response packet.

    Called in ``com.tencent.mobileqq.msf.core.af.a``.

    command name: ``StatSvc.RspMSFForceOffline``

    Note:
        Source: com.tencent.mobileqq.msf.core.af.a

    Args:
        seq (int): Packet sequence.
        session_id (bytes): Session ID.
        ksid (bytes): KSID of client.
        uin (int): User QQ number.
        tgt (bytes): Siginfo tgt.
        d2 (bytes): Siginfo d2.
        d2key (bytes): Siginfo d2 key.
        req_uin (int): Request offline uin.
        seq_no (int): Request sequence number.
        sub_app_id (int): ApkInfo
        device (DeviceInfo): your device info

    Returns:
        Packet: msf force offline response packet.
    """
    COMMAND_NAME = "StatSvc.RspMSFForceOffline"
    SUB_APP_ID = sub_app_id

    resp = ResponseMSFForceOffline(uin=req_uin, seq_no=seq_no, c=bytes(1))
    payload = ResponseMSFForceOffline.to_bytes(0, resp)
    resp_packet = RequestPacketVersion3(
        servant_name="StatSvc",
        func_name="RspMSFForceOffline",
        data=types.MAP(
            {types.STRING("RspMSFForceOffline"): types.BYTES(payload)}
        ),
    ).encode()
    sso_packet = CSsoBodyPacket.build(
        seq,
        SUB_APP_ID,
        COMMAND_NAME,
        device.imei,
        session_id,
        ksid,
        body=resp_packet,
        extra_data=tgt,
    )
    packet = CSsoDataPacket.build(uin, 1, sso_packet, key=d2key, extra_data=d2)
    return packet


async def handle_request_offline(
    client: "Client", packet: IncomingPacket, device: Tuple[DeviceInfo, ApkInfo]
) -> MSFForceOfflineCommand:
    request = MSFForceOfflineCommand.decode_response(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
    )
    logger.error(
        f"Client {client.uin} force offline: " + request.request.info
        if isinstance(request, MSFForceOffline)
        else "Unknown reason."
    )
    if isinstance(request, MSFForceOffline):
        seq = client.next_seq()
        resp_packet = encode_force_offline_response(
            seq,
            client._session_id,
            client._ksid,
            client.uin,
            client._siginfo.tgt,
            client._siginfo.d2,
            client._siginfo.d2key,
            request.request.uin,
            request.request.seq_no,
            device[1].sub_app_id,
            device[0],
        )
        await client.send(seq, "StatSvc.RspMSFForceOffline", resp_packet)
    client._status = OnlineStatus.Offline
    await client.close()
    return request


__all__ = [
    "encode_register",
    "encode_set_status",
    "handle_register_response",
    "handle_request_offline",
    "OnlineStatus",
    "RegPushReason",
    "SvcRegisterResponse",
    "RegisterSuccess",
    "RegisterFail",
    "MSFForceOfflineCommand",
    "MSFForceOffline",
    "MSFForceOfflineError",
]
