"""Binary Tools

This module is used to build Binary tools.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
from typing import Type, Union, TypeVar

P = TypeVar("P", bound="Packet")


class Packet(bytearray):
    """Simple Packet Class

    Inherit from :class:`bytearray`
    """

    @classmethod
    def build(cls: Type[P], *data: Union[bytes, "Packet"]) -> P:
        """Build new packet and write data into it.

        Args:
            *data (Union[:obj:`bytes`, :obj:`Packet`]): Data to write

        Returns:
            :obj:`.Packet`: Current Packet
        """
        return cls().write(*data)

    def write(self: P, *data: Union[bytes, "Packet"]) -> P:
        """Write data into current packet.

        Args:
            *data (Union[:obj:`bytes`, :obj:`Packet`]): Data to write

        Returns:
            :obj:`.Packet`: Current Packet
        """
        for i in data:
            self.extend(i)
        return self
