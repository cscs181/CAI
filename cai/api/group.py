"""Application Group APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import List, Union, Optional

from .base import BaseAPI
from cai.client import GroupMember, Group as group_t

class Group(BaseAPI):
    async def get_group(
        self, group_id: int, cache: bool = True
    ) -> Optional[group_t]:
        """Get Group.

        This function wraps the :meth:`~cai.client.client.Client.get_group`
        method of the client.

        Args:
            group_id (int): Group id.
            cache (bool, optional):  Use cached friend group list. Defaults to True.

        Returns:
            Group: Group object.
            None: Group not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend list failed.
            FriendListException: Get friend list returned non-zero ret code.
        """
        return await self._executor("get_group", group_id, cache)


    async def get_group_list(
        self, cache: bool = True
    ) -> List[group_t]:
        """Get account group list.

        This function wraps the :meth:`~cai.client.client.Client.get_group_list`
        method of the client.

        Args:
            cache (bool, optional): Use cached group list. Defaults to True.

        Returns:
            List[Group]: Group list.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get group list failed.
            GroupListException: Get group list returned non-zero ret code.
        """
        return await self._executor("get_group_list", cache)

    async def get_group_member_list(
        self, group: Union[int, group_t], cache: bool = True
    ) -> Optional[List[GroupMember]]:
        """Get account group member list.

        This function wraps the :meth:`~cai.client.client.Client.get_group_member_list`
        method of the client.

        Args:
            group (Union[int, Group]): Group id or group object want to get members.
            cache (bool, optional): Use cached group list. Defaults to True.

        Returns:
            List[GroupMember]: Group member list.
            None: Group not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get group list failed.
            GroupMemberListException: Get group member list returned non-zero ret code.
        """
        return await self._executor("get_group_member_list", group, cache)


__all__ = ["Group"]
