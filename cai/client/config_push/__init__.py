"""ConfigPushSvc Related SDK.

This module is used to build and handle config push service related packet.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""

from typing import TYPE_CHECKING

from cai.log import logger
from cai.client.packet import IncomingPacket

from .jce import FileServerPushList
from .event import ConfigPushEvent, SsoServerPushEvent, FileServerPushEvent

if TYPE_CHECKING:
    from cai.client import Client


def encode_config_push_response():
    pass


# ConfigPushSvc.PushReq
def handle_config_push_request(
    client: "Client", packet: IncomingPacket
) -> ConfigPushEvent:
    event = ConfigPushEvent.decode_push_req(
        packet.uin, packet.seq, packet.ret_code, packet.command_name,
        packet.data
    )
    if isinstance(event, SsoServerPushEvent):
        logger.debug(f"ConfigPush: Got new server addresses.")
    elif isinstance(event, FileServerPushEvent):
        client._file_storage_info = event.list

    return event


__all__ = [
    "decode_push_req", "FileServerPushList", "ConfigPushEvent",
    "SsoServerPushEvent", "FileServerPushEvent"
]
