"""Application Friend APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import List, Optional

from .base import BaseAPI
from cai.client import FriendGroup, Friend as friend_t


class Friend(BaseAPI):
    async def get_friend(
        self, friend_uin: int, cache: bool = True
    ) -> Optional[friend_t]:
        """Get account friend.

        This function wraps the :meth:`~cai.client.client.Client.get_friend`
        method of the client.

        Args:
            friend_uin (int): Friend account uin.
            cache (bool, optional):  Use cached friend list. Defaults to True.

        Returns:
            Friend: Friend object.
            None: Friend not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend list failed.
            FriendListException: Get friend list returned non-zero ret code.
        """
        return await self.client.get_friend(friend_uin, cache)

    async def get_friend_list(
        self, cache: bool = True
    ) -> List[friend_t]:
        """Get account friend list.

        This function wraps the :meth:`~cai.client.client.Client.get_friend_list`
        method of the client.

        Args:
            cache (bool, optional):  Use cached friend list. Defaults to True.

        Returns:
            List of :obj:`~cai.client.models.Friend`

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend list failed.
            FriendListException: Get friend list returned non-zero ret code.
        """
        return await self._executor("get_friend_list", cache)

    async def get_friend_group(
        self, group_id: int, cache: bool = True
    ) -> Optional[FriendGroup]:
        """Get Friend Group.

        This function wraps the :meth:`~cai.client.client.Client.get_friend_group`
        method of the client.

        Args:
            group_id (int): Friend group id.
            cache (bool, optional):  Use cached friend group list. Defaults to True.

        Returns:
            FriendGroup: Friend group object.
            None: Friend group not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend list failed.
            FriendListException: Get friend list returned non-zero ret code.
        """
        return await self._executor("get_friend_group", group_id, cache)

    async def get_friend_group_list(
        self, cache: bool = True
    ) -> List[FriendGroup]:
        """Get account friend group list.

        This function wraps the :meth:`~cai.client.client.Client.get_friend_group_list`
        method of the client.

        Args:
            cache (bool, optional):  Use cached friend group list. Defaults to True.

        Returns:
            List[FriendGroup]: Friend group list.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend group list failed.
            FriendListException: Get friend group list returned non-zero ret code.
        """
        return await self._executor("get_friend_group_list", cache)


__all__ = [
    "Friend"
]
