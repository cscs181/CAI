"""ConfigPushSvc Related SDK.

This module is used to build and handle config push service related packet.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""

from cai.client.packet import IncomingPacket

from .event import ConfigPushEvent, SsoServerPushEvent, FileServerPushEvent


# ConfigPushSvc.PushReq
def decode_push_req(packet: IncomingPacket) -> ConfigPushEvent:
    return ConfigPushEvent.decode_push_req(
        packet.uin, packet.seq, packet.ret_code, packet.command_name,
        packet.data
    )


__all__ = [
    "decode_push_req", "ConfigPushEvent", "SsoServerPushEvent",
    "FileServerPushEvent"
]
