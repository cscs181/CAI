from enum import IntEnum


class ImageType(IntEnum):
    img = 1000
    gif = 2000
    # jpg = 1003

    def _missing_(cls, value: object):
        return cls.img
