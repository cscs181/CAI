"""Application APIs.

This module wraps the client methods to provide easier control (high-level api).

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import Dict

from cai.client import Client

_clients: Dict[int, Client] = {}


from .client import get_client, close, close_all, set_status
from .login import (
    login,
    submit_captcha,
    submit_slider_ticket,
    request_sms,
    submit_sms,
)
from .friend import (
    get_friend,
    get_friend_list,
    get_friend_group,
    get_friend_group_list,
)
from .group import get_group, get_group_list, get_group_member_list
from .flow import register_packet_handler
