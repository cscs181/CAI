"""Application Exceptions

This module is used to collect all application exceptions.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""


class CaiException(Exception):
    """Application Base Exception"""


class SsoServerException(CaiException):
    """Server Related Exception"""
