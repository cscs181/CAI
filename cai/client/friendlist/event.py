"""Friend List Event Parser.

This module is used to parse friend list packets into event.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from dataclasses import dataclass

from cai.client.event import Event
from cai.utils.jce import RequestPacketVersion3

from .jce import FriendListResp, TroopListRespV2


@dataclass
class FriendListEvent(Event):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "FriendListEvent":
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
            return FriendListEvent(uin, seq, ret_code, command_name)

        try:
            resp_packet = RequestPacketVersion3.decode(data)
            friend_list_response = FriendListResp.decode(
                resp_packet.data["FLRESP"][1:-1]
            )
            if friend_list_response.result == 1:
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
class FriendListSuccess(FriendListEvent):
    response: FriendListResp


@dataclass
class FriendListFail(FriendListEvent):
    result: int
    message: str


@dataclass
class TroopListEvent(Event):
    @classmethod
    def decode_response(
        cls, uin: int, seq: int, ret_code: int, command_name: str, data: bytes
    ) -> "TroopListEvent":
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
            return TroopListEvent(uin, seq, ret_code, command_name)

        try:
            resp_packet = RequestPacketVersion3.decode(data)
            troop_list_response = TroopListRespV2.decode(
                resp_packet.data["GetTroopListRespV2"][1:-1]
            )
            if troop_list_response.result == 1:
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
class TroopListSuccess(TroopListEvent):
    response: TroopListRespV2


@dataclass
class TroopListFail(TroopListEvent):
    result: int
    message: str
