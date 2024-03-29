"""Client Base Command.

This module is used to build command from packet.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

import abc


class Event(abc.ABC):
    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedError
