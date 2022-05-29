from enum import IntEnum


class ImageType(IntEnum):
    jpg = 1000
    png = 1001
    webp = 1002
    bmp = 1005
    gif = 2000
    apng = 2001

    @classmethod
    def _missing_(cls, value: object):
        return cls.jpg
