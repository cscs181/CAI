"""Binary Tools.

This module is used to build Binary tools.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import struct
from typing_extensions import Unpack, TypeVarTuple
from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Type,
    Tuple,
    Union,
    Generic,
    NewType,
    TypeVar,
    Callable,
)

P = TypeVar("P", bound="BasePacket")
Ts = TypeVarTuple("Ts")

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

    def unpack_from(
        self, format: Union[bytes, str], offset: int = 0
    ) -> Tuple[Any, ...]:
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


class Packet(BasePacket, Generic[Unpack[Ts]]):
    """Packet Class for extracting data more efficiently.

    Support `PEP646`_ typing hints. Using ``pyright`` or ``pylance`` for type checking.

    Example:
        >>> packet = Packet(bytes.fromhex("01000233000000"))
        >>> packet.start().int8().uint16().bytes(4).execute()
        (1, 2, b'3\x00\x00\x00')

    .. _PEP646:
        https://www.python.org/dev/peps/pep-0646/

    """

    if TYPE_CHECKING:

        def __new__(cls, *args, **kwargs) -> "Packet[()]":
            ...

    def __init__(self: "Packet[Unpack[Ts]]", *args, **kwargs):
        super(Packet, self).__init__(*args, **kwargs)
        self.start()

    def _add_filter(self, filter: Callable[[Any], Any]):
        self._filters.append(filter)

    def _get_position(self) -> int:
        return struct.calcsize(self._query) + self._offset

    def start(self: "Packet[Unpack[Ts]]", offset: int = 0) -> "Packet[()]":
        self._query: str = ">"
        self._offset: int = offset
        self._executed: bool = False
        self._filters: List[Callable[[Any], Any]] = []
        return self  # type: ignore

    def bool(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], BOOL]":
        self._query += "?"
        self._add_filter(BOOL)
        return self  # type: ignore

    def int8(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], INT8]":
        self._query += "b"
        self._add_filter(INT8)
        return self  # type: ignore

    def uint8(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], UINT8]":
        self._query += "B"
        self._add_filter(UINT8)
        return self  # type: ignore

    def int16(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], INT16]":
        self._query += "h"
        self._add_filter(INT16)
        return self  # type: ignore

    def uint16(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], UINT16]":
        self._query += "H"
        self._add_filter(UINT16)
        return self  # type: ignore

    def int32(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], INT32]":
        self._query += "i"
        self._add_filter(INT32)
        return self  # type: ignore

    def uint32(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], UINT32]":
        self._query += "I"
        self._add_filter(UINT32)
        return self  # type: ignore

    def int64(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], INT64]":
        self._query += "q"
        self._add_filter(INT64)
        return self  # type: ignore

    def uint64(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], UINT64]":
        self._query += "Q"
        self._add_filter(UINT64)
        return self  # type: ignore

    def float(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], FLOAT]":
        self._query += "f"
        self._add_filter(FLOAT)
        return self  # type: ignore

    def double(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], DOUBLE]":
        self._query += "d"
        self._add_filter(DOUBLE)
        return self  # type: ignore

    def byte(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], BYTE]":
        self._query += "c"
        self._add_filter(BYTE)
        return self  # type: ignore

    def bytes(
        self: "Packet[Unpack[Ts]]", length: int
    ) -> "Packet[Unpack[Ts], BYTES]":
        self._query += f"{length}s"
        self._add_filter(BYTES)
        return self  # type: ignore

    def bytes_with_length(
        self: "Packet[Unpack[Ts]]", head_bytes: int, offset: int = 0
    ) -> "Packet[Unpack[Ts], BYTES]":
        length = int.from_bytes(
            self.read_bytes(head_bytes, self._get_position()),
            "big",
        )
        self._query += f"{head_bytes}x{length - offset}s"
        self._add_filter(BYTES)
        return self  # type: ignore

    def string(
        self: "Packet[Unpack[Ts]]",
        head_bytes: int,
        offset: int = 0,
        encoding: str = "utf-8",
    ) -> "Packet[Unpack[Ts], STRING]":
        length = int.from_bytes(
            self.read_bytes(head_bytes, self._get_position()),
            "big",
        )
        self._query += f"{head_bytes}x{length - offset}s"
        self._add_filter(lambda x: STRING(x.decode(encoding)))
        return self  # type: ignore

    def offset(self: "Packet[Unpack[Ts]]", offset: int) -> "Packet[Unpack[Ts]]":
        self._query += f"{offset}x"
        return self

    def remain(self: "Packet[Unpack[Ts]]") -> "Packet[Unpack[Ts], Packet[()]]":
        length = struct.calcsize(self._query)
        self._query += f"{len(self) - length}s"
        self._add_filter(Packet)
        return self  # type: ignore

    def execute(self: "Packet[Unpack[Ts]]") -> Tuple[Unpack[Ts]]:
        if self._executed:
            raise RuntimeError("Cannot re-execute query. Call `start()` first.")
        query = self._query
        filters = self._filters
        self._query = ">"
        self._filters = []
        self._executed = True
        return tuple(
            map(
                lambda f, v: f(v),
                filters,
                self.unpack_from(query, self._offset),
            )
        )  # type: ignore
