"""Application Logger

This module is used to build application logger.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import logging

logger = logging.getLogger("cai")
network = logging.getLogger("cai.network")
highway = logging.getLogger("cai.highway")
