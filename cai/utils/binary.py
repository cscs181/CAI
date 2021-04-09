"""Binary Tools.

This module is used to build Binary tools.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import struct
from typing import Any, List, Type, Tuple, Union, TypeVar, Optional, Callable, NewType

P = TypeVar("P", bound="BasePacket")

BOOL = NewType("BOOL", bool)
INT8 = NewType("INT8", int)
UINT8 = NewType("UINT8", int)
INT16 = NewType("INT16", int)
UINT16 = NewType("UINT16", int)
INT32 = NewType("INT32", int)
UINT32 = NewType("UINT32", int)
INT64 = NewType("INT64", int)
UINT64 = NewType("UINT64", int)
FLOAT = NewType("FLOAT", float)
DOUBLE = NewType("DOUBLE", float)
BYTE = NewType("BYTE", bytes)
BYTES = NewType("BYTES", bytes)
STRING = NewType("STRING", str)


class BasePacket(bytearray):
    """Base Packet Class.

    Provides basic operations like reading, writing by offset.

    Inherit from :class:`bytearray`
    """

    @classmethod
    def build(cls: Type[P], *data: Union[bytes, "BasePacket"]) -> P:
        """Build new packet and write data into it.

        Args:
            *data (Union[:obj:`bytes`, :obj:`Packet`]): Data to write

        Returns:
            :obj:`.Packet`: Current Packet
        """
        return cls().write(*data)

    def write(self: P, *data: Union[bytes, "BasePacket"]) -> P:
        """Write data into current packet.

        Args:
            *data (Union[:obj:`bytes`, :obj:`Packet`]): Data to write

        Returns:
            :obj:`.Packet`: Current Packet
        """
        for i in data:
            self.extend(i)
        return self

    def write_with_length(
        self: P, *data: Union[bytes, "BasePacket"], offset: int = 0
    ) -> P:
        """Write data into current packet with 4-byte length.

        Args:
            *data (Union[:obj:`bytes`, :obj:`Packet`]): Data to write
            offset (int): Length offset

        Returns:
            :obj:`.Packet`: Current Packet
        """
        self.extend(struct.pack(">I", sum(map(len, data)) + offset))
        return self.write(*data)

    def unpack(self, format: Union[bytes, str]) -> Tuple[Any, ...]:
        """Unpack all data from current packet.

        Args:
            format (Union[bytes, str]): Struct format.

        Returns:
            Tuple[Any, ...]: Unpacked data tuple.
        """
        return struct.unpack(format, self)

    def unpack_from(self,
                    format: Union[bytes, str],
                    offset: int = 0) -> Tuple[Any, ...]:
        """Unpack data from current packet with given offset.

        Args:
            format (Union[bytes, str]): Struct format.
            offset (int, optional): Data offset. Defaults to 0.

        Returns:
            Tuple[Any, ...]: Unpacked data.
        """
        return struct.unpack_from(format, self, offset)

    def read_int8(self, offset: int = 0) -> INT8:
        return struct.unpack_from(">b", self, offset)[0]

    def read_uint8(self, offset: int = 0) -> UINT8:
        return struct.unpack_from(">B", self, offset)[0]

    def read_int16(self, offset: int = 0) -> INT16:
        return struct.unpack_from(">h", self, offset)[0]

    def read_uint16(self, offset: int = 0) -> UINT16:
        return struct.unpack_from(">H", self, offset)[0]

    def read_int32(self, offset: int = 0) -> INT32:
        return struct.unpack_from(">i", self, offset)[0]

    def read_uint32(self, offset: int = 0) -> UINT32:
        return struct.unpack_from(">I", self, offset)[0]

    def read_int64(self, offset: int = 0) -> INT64:
        return struct.unpack_from(">q", self, offset)[0]

    def read_uint64(self, offset: int = 0) -> UINT64:
        return struct.unpack_from(">Q", self, offset)[0]

    def read_byte(self, offset: int = 0) -> BYTE:
        return struct.unpack_from(">c", self, offset)[0]

    def read_bytes(self, n: int, offset: int = 0) -> BYTES:
        return struct.unpack_from(f">{n}s", self, offset)[0]

    def read_string(self, offset: int = 0) -> STRING:
        length = self.read_int32(offset) - 4
        return STRING(self.read_bytes(length, offset + 4).decode())


class Packet(BasePacket):
    """Packet Class for extracting data more efficiently.

    Support `PEP646`_ typing hints. Using ``pyright`` or ``pylance`` for type checking.

    Example:
        >>> packet = Packet(bytes.fromhex("01000233000000"))
        >>> packet.int8().uint16().bytes(4).execute()
        (1, 2, b'3\x00\x00\x00')

    .. _PEP646:
        https://www.python.org/dev/peps/pep-0646/

    """

    def __init__(
        self, *args, cache: Optional[Tuple[Any, ...]] = None, **kwargs
    ):
        super(Packet, self).__init__(*args, **kwargs)
        self._query = ">"
        self._cache = cache or tuple()
        self._filters: List[Callable[[Any], Any]] = []

    def _add_filter(self, filter: Callable[[Any], Any]):
        self._filters.append(filter)

    def bool(self):
        self._query += "?"
        self._add_filter(BOOL)
        return self

    def int8(self):
        self._query += "b"
        self._add_filter(INT8)
        return self

    def uint8(self):
        self._query += "B"
        self._add_filter(UINT8)
        return self

    def int16(self):
        self._query += "h"
        self._add_filter(INT16)
        return self

    def uint16(self):
        self._query += "H"
        self._add_filter(UINT16)
        return self

    def int32(self):
        self._query += "i"
        self._add_filter(INT32)
        return self

    def uint32(self):
        self._query += "I"
        self._add_filter(UINT32)
        return self

    def int64(self):
        self._query += "q"
        self._add_filter(INT64)
        return self

    def uint64(self):
        self._query += "Q"
        self._add_filter(UINT64)
        return self

    def float(self):
        self._query += "f"
        self._add_filter(FLOAT)
        return self

    def double(self):
        self._query += "d"
        self._add_filter(DOUBLE)
        return self

    def byte(self):
        self._query += "c"
        self._add_filter(BYTE)
        return self

    def bytes(self, length: int):
        self._query += f"{length}s"
        self._add_filter(BYTES)
        return self

    def string(self, head_bytes: int, encoding: str = "utf-8"):
        self._query += f"{head_bytes}s"
        self._add_filter(BYTES)
        packet = self._exec_cache()
        length = int.from_bytes(packet._cache[-1], "big")
        packet._cache = packet._cache[:-1]
        packet._query += f"{length}s"
        packet._add_filter(lambda x: STRING(x.decode(encoding)))
        return packet

    def offset(self, offset: int):
        self._query += f"{offset}x"
        return self

    def _exec_cache(self):
        length = struct.calcsize(self._query)
        cache = self.execute()
        return Packet(self[length:], cache=cache)

    def execute(self):
        query = self._query
        filters = self._filters
        self._query = ">"
        self._filters = []
        return self._cache + tuple(
            map(lambda f, v: f(v), filters, self.unpack_from(query))
        )
