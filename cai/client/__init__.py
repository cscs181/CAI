"""Application Client.

This module is main entry point for the application.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from .event import Event
from .packet import IncomingPacket
from .client import Client, HANDLERS
from .models import Friend, Group
from .status_service import OnlineStatus, RegPushReason
