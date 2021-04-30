"""MessageSvc Related SDK.

This module is used to build and handle message service related packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import TYPE_CHECKING

from cai.log import logger
from cai.utils.binary import Packet
from cai.client.packet import IncomingPacket
from cai.client.status_service import OnlineStatus
from .event import (
    PushNotifyEvent,
    PushNotify,
    PushNotifyError,
    PushForceOfflineEvent,
    PushForceOffline,
    PushForceOfflineError,
)

if TYPE_CHECKING:
    from cai.client import Client


# TODO
async def encode_get_message() -> Packet:
    ...


async def handle_push_notify(
    client: "Client", packet: IncomingPacket
) -> PushNotifyEvent:
    notify = PushNotifyEvent.decode_response(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
    )
    print(notify)
    return notify


# MessageSvc.PushForceOffline
async def handle_force_offline(
    client: "Client", packet: IncomingPacket
) -> PushForceOfflineEvent:
    client._status = OnlineStatus.Offline
    await client.close()
    request = PushForceOfflineEvent.decode_response(
        packet.uin,
        packet.seq,
        packet.ret_code,
        packet.command_name,
        packet.data,
    )
    logger.error(
        f"Client {client.uin} force offline: " + request.request.tips
        if isinstance(request, PushForceOffline)
        else "Unknown reason."
    )
    return request


__all__ = [
    "handle_push_notify",
    "PushNotifyEvent",
    "PushNotify",
    "PushNotifyError",
    "handle_force_offline",
    "PushForceOfflineEvent",
    "PushForceOffline",
    "PushForceOfflineError",
]
