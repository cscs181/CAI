"""Client packets.

This module is used to packet data into outgoing format.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import zlib
import struct
from dataclasses import dataclass
from typing import Union, Optional

from rtea import qqtea_encrypt, qqtea_decrypt

from cai.utils.ecdh import ECDH
from cai.utils.binary import Packet


class CSsoBodyPacket(Packet):
    """CSSOBody Packet.

    Note:
        Source:
            com.tencent.qphone.base.util.CodecWarpper

            /data/data/com.tencent.mobileqq/lib/libcodecwrapperV2.so

            `CSSOReqHead::serialize_verFull`
    """

    @classmethod
    def build(
        cls,
        seq: int,
        sub_app_id: int,
        command_name: str,
        imei: str,
        session_id: bytes,
        ksid: bytes,
        body: Union[bytes, Packet],
        extra_data: Union[bytes, Packet] = b"",
        unknown_bytes: bytes = bytes(
            [
                0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x01, 0x00
            ]
        )
    ) -> "CSsoBodyPacket":
        """Build CSSOBody head and append body.

        Note:
            Source: `CSSOReqHead::serialize_verFull`
        """
        extra = extra_data and (len(extra_data) != 4)
        packet = cls().write_with_length(
            struct.pack(">III", seq, sub_app_id, sub_app_id),
            unknown_bytes,
            struct.pack(">I", 4) if not extra else b"",
            struct.pack(
                ">I",
                len(extra_data) + 4,
            ) if extra else b"",
            extra_data if extra else b"",
            struct.pack(">I",
                        len(command_name) + 4),
            command_name.encode(),
            struct.pack(">I",
                        len(session_id) + 4),
            session_id,
            struct.pack(">I",
                        len(imei) + 4),
            imei.encode(),
            struct.pack(">IH", 4,
                        len(ksid) + 2),
            ksid,
            struct.pack(">I", 4),
            offset=4
        )
        return packet.write_with_length(body, offset=4)


class CSsoDataPacket(Packet):
    """CSSOData Packet.

    `KSSOVersion`: `Full: 0xA` `Simple: 0xB`.

    Note:
        Source:
            com.tencent.qphone.base.util.CodecWarpper

            /data/data/com.tencent.mobileqq/lib/libcodecwrapperV2.so

            `CSSOData::serialize`
    """

    @classmethod
    def build(
        cls,
        uin: int,
        body_type: int,
        body: Union[bytes, Packet],
        ksso_version: int = 0xA,
        key: Optional[bytes] = None,
        extra_data: bytes = b""
    ) -> "CSsoDataPacket":
        """Build CSSOPacket head and append body.

        Packet body was encrypted in `CSSOData::serialize`.

        Note:
            Source: `CSSOHead::serialize_verFull`
        """
        return cls().write_with_length(
            Packet.build(
                struct.pack(">IB", ksso_version, body_type),
                struct.pack(">I",
                            len(extra_data) + 4), extra_data, bytes([0]),
                struct.pack(">I",
                            len(str(uin)) + 4),
                str(uin).encode(),
                qqtea_encrypt(body, key) if key else body
            ),
            offset=4
        )


class UniPacket(Packet):

    @classmethod
    def build(
        cls,
        uin: int,
        seq: int,
        command_name: str,
        session_id: bytes,
        encrypt_type: int,
        body: Union[bytes, Packet],
        key: bytes,
        extra_data: bytes = b""
    ) -> "UniPacket":
        data = Packet().write_with_length(
            struct.pack(">I",
                        len(command_name) + 4),
            command_name.encode(),
            struct.pack(">I",
                        len(session_id) + 4),
            session_id,
            struct.pack(">I",
                        len(extra_data) + 4),
            extra_data,
            offset=4
        )
        data.write_with_length(body, offset=4)
        return cls().write_with_length(
            struct.pack(">IBIB", 0xB, encrypt_type, seq, 0),
            struct.pack(">I",
                        len(str(uin)) + 4),
            str(uin).encode(), qqtea_encrypt(data, key)
        )


@dataclass
class IncomingPacket:
    uin: int
    seq: int
    ret_code: int
    extra: bytes
    command_name: str
    session_id: bytes
    data: bytes

    @classmethod
    def parse(
        cls, data: Union[bytes, Packet], key: bytes, d2key: bytes,
        session_key: bytes
    ) -> "IncomingPacket":
        if not isinstance(data, Packet):
            data = Packet(data)

        offset = 0

        packet_type, encrypt_type, flag3 = data.unpack_from(">IBB", offset)
        offset += 6
        if packet_type not in [0xA, 0xB]:
            raise ValueError(
                f"Invalid packet type. Expected 0xA / 0xB, got {packet_type}."
            )
        if flag3 != 0:
            raise ValueError(f"Invalid flag3. Expected 0, got {flag3}.")

        uin = data.read_string(offset)
        offset += 4 + len(uin)
        try:
            uin = int(uin)
        except ValueError:
            uin = 0

        payload: Packet
        if encrypt_type == 0:
            payload = Packet(data[offset:])
        elif encrypt_type == 1:
            payload = Packet(qqtea_decrypt(data[offset:], d2key))
        elif encrypt_type == 2:
            payload = Packet(qqtea_decrypt(data[offset:], bytes(16)))
        else:
            raise ValueError(
                f"Invalid encrypt type. Expected 0 / 1 / 2, got {encrypt_type}."
            )

        if not payload:
            raise ValueError(f"Data cannot be none.")

        offset = 0
        sso_frame_length = payload.read_int32(offset) - 4
        offset += 4
        sso_frame = payload.read_bytes(sso_frame_length, offset)

        return cls.parse_sso_frame(
            sso_frame, encrypt_type, key, session_key, uin=uin
        )

    @classmethod
    def parse_sso_frame(
        cls, sso_frame: Union[bytes, Packet], encrypt_type: int, key: bytes,
        session_key: bytes, **kwargs
    ) -> "IncomingPacket":
        if not isinstance(sso_frame, Packet):
            sso_frame = Packet(sso_frame)

        offset = 0
        seq = sso_frame.read_int32(offset)
        offset += 4
        ret_code = sso_frame.read_int32(offset)
        offset += 4

        extra_length = sso_frame.read_int32(offset) - 4
        offset += 4
        extra = sso_frame.read_bytes(extra_length, offset)
        offset += extra_length

        command_name = sso_frame.read_string(offset)
        offset += 4 + len(command_name)

        session_id_length = sso_frame.read_int32(offset)
        offset += 4
        session_id = sso_frame.read_bytes(session_id_length, offset)
        offset += session_id_length

        compress_type = sso_frame.read_int32(offset)
        offset += 4
        decompressed_data: bytes
        if compress_type == 0:
            # data_length = sso_frame.read_int32(offset)
            # if data_length == len(sso_frame) - offset or data_length == len(
            #     sso_frame
            # ) - offset - 4:
            #     decompressed_data = sso_frame[offset + 4:]
            # else:
            #     decompressed_data = sso_frame[offset + 4:]
            decompressed_data = sso_frame[offset + 4:]
        elif compress_type == 1:
            decompressed_data = zlib.decompress(sso_frame[offset + 4:])
        elif compress_type == 8:
            decompressed_data = sso_frame[offset + 4:]
        else:
            raise ValueError(f"Unknown compression type, got {compress_type}.")

        if encrypt_type == 2:
            decompressed_data = cls.parse_oicq_body(
                decompressed_data, key, session_key
            )

        return cls(
            seq=seq,
            ret_code=ret_code,
            extra=extra,
            command_name=command_name,
            session_id=session_id,
            data=decompressed_data,
            **kwargs
        )

    @classmethod
    def parse_oicq_body(
        cls, data: Union[bytes, Packet], key: bytes, session_key: bytes
    ) -> bytes:
        if not isinstance(data, Packet):
            data = Packet(data)

        flag = data.read_uint8()
        if not flag != 2:
            raise ValueError(
                f"Invalid OICQ response flag. Expected 2, got {flag}."
            )

        offset = 13
        encrypt_type = data.read_uint16(offset)
        offset += 2 + 1

        body = data[offset:-1]
        if encrypt_type == 0:
            try:
                return qqtea_decrypt(body, ECDH.share_key)
            except Exception:
                return qqtea_decrypt(body, key)
        elif encrypt_type == 3:
            return qqtea_decrypt(body, session_key)
        elif encrypt_type == 4:
            # seems not used
            # data = qqtea_decrypt(body, ECDH.share_key)
            # ...
            raise NotImplementedError
        else:
            raise ValueError(f"Unknown encrypt type: {encrypt_type}")
