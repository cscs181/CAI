"""Crypto Tool.

This module is used to encrypt data using ECDH or Session ticket encryption.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import struct
from hashlib import md5
from typing import Union

from rtea import qqtea_encrypt
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from cai.utils.binary import Packet


class ECDH:
    id = 0x87
    _p256 = ec.SECP256R1()

    svr_public_key = ec.EllipticCurvePublicKey.from_encoded_point(
        _p256,
        bytes.fromhex(
            "04"
            "EBCA94D733E399B2DB96EACDD3F69A8BB0F74224E2B44E3357812211D2E62EFB"
            "C91BB553098E25E33A799ADC7F76FEB208DA7C6522CDB0719A305180CC54A82E"
        ),
    )

    client_private_key = ec.generate_private_key(_p256)
    client_public_key = client_private_key.public_key().public_bytes(
        Encoding.X962, PublicFormat.UncompressedPoint
    )

    share_key = md5(
        client_private_key.exchange(ec.ECDH(), svr_public_key)[:16]
    ).digest()

    @classmethod
    def encrypt(
        cls, data: Union[bytes, Packet], key: Union[bytes, Packet]
    ) -> Packet:
        return Packet.build(
            struct.pack(">BB", 2, 1),
            key,
            struct.pack(
                ">HHH",
                305,
                1,  # oicq.wlogin_sdk.tools.EcdhCrypt.sKeyVersion
                len(cls.client_public_key),
            ),
            cls.client_public_key,
            qqtea_encrypt(bytes(data), cls.share_key),
        )


class EncryptSession:
    id = 0x45

    def __init__(self, ticket: bytes):
        self.ticket = ticket

    def encrypt(
        self, data: Union[bytes, Packet], key: Union[bytes, Packet]
    ) -> Packet:
        return Packet.build(
            struct.pack(">H", len(self.ticket)),
            self.ticket,
            qqtea_encrypt(bytes(data), bytes(key)),
        )
