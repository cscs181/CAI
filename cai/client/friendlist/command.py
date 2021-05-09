"""Friend List Command Parser.

This module is used to parse friend list packets into command.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from dataclasses import dataclass

from cai.client.command import Command
from cai.utils.jce import RequestPacketVersion3

from .jce import FriendListResp, TroopListRespV2, TroopMemberListResp


@dataclass
class FriendListCommand(Command):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "FriendListCommand":
        """Decode friend list response.

        Note:
            Source: com.tencent.mobileqq.service.friendlist.FriendListService.h

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.

        Returns:
            FriendSuccess: Friend list success.
            FriendFail: Friend list failed.
        """
        if ret_code != 0 or not data:
            return FriendListCommand(uin, seq, ret_code, command_name)

        try:
            resp_packet = RequestPacketVersion3.decode(data)
            friend_list_response = FriendListResp.decode(
                resp_packet.data["FLRESP"][1:-1]  # type: ignore
            )
            if friend_list_response.result != 0:
                return FriendListFail(
                    uin,
                    seq,
                    ret_code,
                    command_name,
                    friend_list_response.result,
                    "Friend list returns non-zero result code",
                )
            return FriendListSuccess(
                uin, seq, ret_code, command_name, friend_list_response
            )
        except Exception as e:
            return FriendListFail(
                uin,
                seq,
                ret_code,
                command_name,
                -1,
                f"Error when decoding response! {repr(e)}",
            )


@dataclass
class FriendListSuccess(FriendListCommand):
    response: FriendListResp


@dataclass
class FriendListFail(FriendListCommand):
    result: int
    message: str


@dataclass
class TroopListCommand(Command):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "TroopListCommand":
        """Decode troop list v2 response.

        Note:
            Source: com.tencent.mobileqq.service.troop.TroopReceiver.c

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.

        Returns:
            TroopListSuccess: Troop list success.
            TroopListFail: Troop list failed.
        """
        if ret_code != 0 or not data:
            return TroopListCommand(uin, seq, ret_code, command_name)

        try:
            resp_packet = RequestPacketVersion3.decode(data)
            troop_list_response = TroopListRespV2.decode(
                resp_packet.data["GetTroopListRespV2"][1:-1]  # type: ignore
            )
            if troop_list_response.result != 0:
                return TroopListFail(
                    uin,
                    seq,
                    ret_code,
                    command_name,
                    troop_list_response.result,
                    "Troop list returns non-zero result code",
                )
            return TroopListSuccess(
                uin, seq, ret_code, command_name, troop_list_response
            )
        except Exception as e:
            return TroopListFail(
                uin,
                seq,
                ret_code,
                command_name,
                -1,
                f"Error when decoding response! {repr(e)}",
            )


@dataclass
class TroopListSuccess(TroopListCommand):
    response: TroopListRespV2


@dataclass
class TroopListFail(TroopListCommand):
    result: int
    message: str


@dataclass
class TroopMemberListCommand(Command):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "TroopMemberListCommand":
        """Decode troop member list response.

        Note:
            Source: com.tencent.mobileqq.service.troop.TroopReceiver.e

        Args:
            uin (int): User QQ
            seq (int): Sequence number of the response packet.
            ret_code (int): Return code of the response.
            command_name (str): Command name of the response.
            data (bytes): Payload data of the response.

        Returns:
            TroopMemberListSuccess: Troop member list success.
            TroopMemberListFail: Troop member list failed.
        """
        if ret_code != 0 or not data:
            return TroopMemberListCommand(uin, seq, ret_code, command_name)

        try:
            resp_packet = RequestPacketVersion3.decode(data)
            troop_member_list_response = TroopMemberListResp.decode(
                resp_packet.data["GTMLRESP"][1:-1]  # type: ignore
            )
            if troop_member_list_response.result != 0:
                return TroopMemberListFail(
                    uin,
                    seq,
                    ret_code,
                    command_name,
                    troop_member_list_response.result,
                    "Troop list returns non-zero result code",
                )
            return TroopMemberListSuccess(
                uin, seq, ret_code, command_name, troop_member_list_response
            )
        except Exception as e:
            return TroopMemberListFail(
                uin,
                seq,
                ret_code,
                command_name,
                -1,
                f"Error when decoding response! {repr(e)}",
            )


@dataclass
class TroopMemberListSuccess(TroopMemberListCommand):
    response: TroopMemberListResp


@dataclass
class TroopMemberListFail(TroopMemberListCommand):
    result: int
    message: str
