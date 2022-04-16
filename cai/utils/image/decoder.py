import struct
import binascii
from typing import BinaryIO
from dataclasses import dataclass

from .enum import ImageType


@dataclass
class ImageInfo:
    name: str
    width: int
    height: int
    depth: int

    @property
    def pic_type(self) -> ImageType:
        return getattr(ImageType, self.name)


class BaseDecoder:
    @classmethod
    def decode(cls, fio: BinaryIO) -> ImageInfo:
        raise NotImplementedError


class JPEGDecoder(BaseDecoder):
    @classmethod
    def decode(cls, fio: BinaryIO) -> ImageInfo:
        if fio.read(2) != b"\xff\xd8":
            raise TypeError("not a valid jpeg file")
        while True:
            if fio.read(1) != b"\xff":
                raise ValueError("decoder fail")
            btype = fio.read(1)
            data = fio.read(
                int.from_bytes(fio.read(2), "big") - 2
            )
            if btype == b"\xc0":
                depth, height, width, _ = struct.unpack("!BHHB", data[:6])
                print(width, height)
                return ImageInfo("jpg", width, height, depth)


class PNGDecoder(BaseDecoder):
    @classmethod
    def decode(cls, fio: BinaryIO) -> ImageInfo:
        if fio.read(8).hex() != "89504e470d0a1a0a":
            raise TypeError("not a valid png file")
        while True:
            raw_head = fio.read(8)
            if not raw_head:
                break
            elif len(raw_head) != 8:
                raise ValueError("decoder fail")
            length, btype = struct.unpack("!I4s", raw_head)
            data = fio.read(length)
            if binascii.crc32(raw_head[4:] + data) != int.from_bytes(fio.read(4), "big"):
                raise ValueError("CRC not match")
            elif btype == b"IHDR":
                width, height, depth, *_ = struct.unpack("!IIBBBBB", data)
                return ImageInfo("png", width, height, depth)


class GIFDecoder(BaseDecoder):
    @classmethod
    def decode(cls, fio: BinaryIO) -> ImageInfo:
        if fio.read(6) != b"GIF89a":
            raise TypeError("not a valid gif file")
        width, height, flag, *_ = struct.unpack("<HHBBB", fio.read(7))
        return ImageInfo("gif", width, height, ((flag ^ 0x80) >> 4) + 2)


class BMPDecoder(BaseDecoder):
    @classmethod
    def decode(cls, fio: BinaryIO) -> ImageInfo:
        if fio.read(2) != b"BM":
            raise TypeError("not a valid bmp file")
        fio.read(12)  # offset
        data = fio.read(16)
        _, width, height, _, depth = struct.unpack("<IiiHH", data)
        return ImageInfo("bmp", width, height, depth)


def decode(f: BinaryIO) -> ImageInfo:
    head = f.read(3)
    f.seek(0)
    try:
        if head[:-1] == b"\xff\xd8":
            return JPEGDecoder.decode(f)
        elif head.hex() == "89504e":
            return PNGDecoder.decode(f)
        elif head == b"GIF":
            return GIFDecoder.decode(f)
        elif head[:-1] == b"BM":
            return BMPDecoder.decode(f)
        else:
            raise NotImplementedError
    finally:
        f.seek(0)
