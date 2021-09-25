"""Application Group APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import List, Union, Optional

from cai.client import Group, GroupMember

from .client import get_client


async def get_group(
    group_id: int, cache: bool = True, uin: Optional[int] = None
) -> Optional[Group]:
    """Get Group.

    This function wraps the :meth:`~cai.client.client.Client.get_group`
    method of the client.

    Args:
        group_id (int): Group id.
        cache (bool, optional):  Use cached friend group list. Defaults to True.
        uin (Optional[int], optional): Account of the client want to use.
            Defaults to None.

    Returns:
        Group: Group object.
        None: Group not exists.

    Raises:
        RuntimeError: Error response type got. This should not happen.
        ApiResponseError: Get friend list failed.
        FriendListException: Get friend list returned non-zero ret code.
    """
    client = get_client(uin)
    return await client.get_group(group_id, cache)


async def get_group_list(
    cache: bool = True, uin: Optional[int] = None
) -> List[Group]:
    """Get account group list.

    This function wraps the :meth:`~cai.client.client.Client.get_group_list`
    method of the client.

    Args:
        cache (bool, optional): Use cached group list. Defaults to True.
        uin (Optional[int], optional): Account of the client want to use.
            Defaults to None.

    Returns:
        List[Group]: Group list.

    Raises:
        RuntimeError: Error response type got. This should not happen.
        ApiResponseError: Get group list failed.
        GroupListException: Get group list returned non-zero ret code.
    """
    client = get_client(uin)
    return await client.get_group_list(cache)


async def get_group_member_list(
    group: Union[int, Group], cache: bool = True, uin: Optional[int] = None
) -> Optional[List[GroupMember]]:
    """Get account group member list.

    This function wraps the :meth:`~cai.client.client.Client.get_group_member_list`
    method of the client.

    Args:
        group (Union[int, Group]): Group id or group object want to get members.
        cache (bool, optional): Use cached group list. Defaults to True.
        uin (Optional[int], optional): Account of the client want to use.
            Defaults to None.

    Returns:
        List[GroupMember]: Group member list.
        None: Group not exists.

    Raises:
        RuntimeError: Error response type got. This should not happen.
        ApiResponseError: Get group list failed.
        GroupMemberListException: Get group member list returned non-zero ret code.
    """
    client = get_client(uin)
    return await client.get_group_member_list(group, cache)


__all__ = ["get_group", "get_group_list", "get_group_member_list"]
