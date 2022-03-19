"""Application APIs.

This module wraps the client methods to provide easier control (high-level api).

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from .client import Client, make_client


__all__ = ["Client", "make_client"]
