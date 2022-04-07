"""Application Client.

This module is main entry point for the application.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from cai.client.events.base import Event
from .command import Command
from .packet import IncomingPacket
from .client import HANDLERS, Client
from .status_service import OnlineStatus, RegPushReason
from .message_service import GroupMessage, PrivateMessage
from .models import Group, Friend, FriendGroup, GroupMember, GroupMemberRole
