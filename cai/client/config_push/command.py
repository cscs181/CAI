"""ConfigPushSvc Command Parser.

This module is used to parse ConfigPushSvc packets into command.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from dataclasses import dataclass

from cai.client.command import Command
from cai.utils.jce import RequestPacketVersion2

from .jce import PushReq, SsoServerPushList, FileServerPushList


@dataclass
class ConfigPushCommand(Command):
    @classmethod
    def decode_push_req(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "ConfigPushCommand":
        """Decode ConfigPush.PushReq packet.

        Note:
            Source:

            com.tencent.mobileqq.msf.core.a.c.a (type 1)

            com.tencent.mobileqq.servlet.PushServlet.onReceive (type 2)

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.

        Returns:
            SsoServerPushCommand: Push Sso Server Info List.
            FileServerPushCommand: Push File Server Info List.
        """
        if ret_code != 0 or not data:
            return cls(uin, seq, ret_code, command_name)

        packet = RequestPacketVersion2.decode(data)
        push = PushReq.decode(
            packet.data["PushReq"]["ConfigPush.PushReq"][1:-1]  # type: ignore
        )
        if push.type == 1:
            list = SsoServerPushList.decode(push.jcebuf)
            return SsoServerPushCommand(
                uin,
                seq,
                ret_code,
                command_name,
                push.type,
                push.jcebuf,
                push.large_seq,
                list,
            )
        elif push.type == 2:
            list = FileServerPushList.decode(push.jcebuf)
            return FileServerPushCommand(
                uin,
                seq,
                ret_code,
                command_name,
                push.type,
                push.jcebuf,
                push.large_seq,
                list,
            )
        elif push.type == 3:
            # LogAction, do nothing
            return LogActionPushCommand(
                uin,
                seq,
                ret_code,
                command_name,
                push.type,
                push.jcebuf,
                push.large_seq,
            )
        return ConfigPushCommand(uin, seq, ret_code, command_name)


@dataclass
class _ConfigPushCommandBase(ConfigPushCommand):
    type: int
    jcebuf: bytes
    large_seq: int


@dataclass
class SsoServerPushCommand(_ConfigPushCommandBase):
    list: SsoServerPushList


@dataclass
class FileServerPushCommand(_ConfigPushCommandBase):
    list: FileServerPushList


@dataclass
class LogActionPushCommand(_ConfigPushCommandBase):
    pass
