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


from .flow import *
from .group import *
from .login import *
from .client import *
from .friend import *
