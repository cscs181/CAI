"""Application Client APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

import hashlib
from typing import Union, BinaryIO, Optional, Sequence

from cai import log
from cai.client import OnlineStatus
from cai.client import Client as client_t
from cai.settings.device import get_device
from cai.pb.msf.msg.svc import PbSendMsgResp
from cai.client.highway import HighWaySession
from cai.settings.protocol import get_protocol
from cai.client.message_service.encoders import build_msg, make_group_msg_pkg
from cai.client.message.models import (
    Element,
    ImageElement,
    VoiceElement,
)

from .group import Group as _Group
from .login import Login as _Login
from .flow import Events as _Events
from .friend import Friend as _Friend
from .error import (
    BotMutedException,
    AtAllLimitException,
    GroupMsgLimitException,
)


def make_client(uin: int, passwd: Union[str, bytes]) -> client_t:
    if not (isinstance(passwd, bytes) and len(passwd) == 16):
        # not a vailed md5 passwd
        if isinstance(passwd, bytes):
            passwd = hashlib.md5(passwd).digest()
        else:
            passwd = hashlib.md5(passwd.encode()).digest()
    device = get_device(uin)
    apk_info = get_protocol(uin)
    return client_t(uin, passwd, device, apk_info)


class Client(_Login, _Friend, _Group, _Events):
    def __init__(self, client: client_t):
        self.client = client
        self._highway_session = HighWaySession(client, logger=log.highway)

    @property
    def connected(self) -> bool:
        return self.client.connected

    @property
    def status(self) -> Optional[OnlineStatus]:
        return self.client.status

    async def send_group_msg(self, gid: int, msg: Sequence[Element]):
        # todo: split long msg
        resp: PbSendMsgResp = PbSendMsgResp.FromString(
            (
                await self.client.send_unipkg_and_wait(
                    "MessageSvc.PbSendMsg",
                    make_group_msg_pkg(
                        self.client.next_seq(), gid, build_msg(msg)
                    ).SerializeToString(),
                )
            ).data
        )

        if resp.result == 120:
            raise BotMutedException
        elif resp.result == 121:
            raise AtAllLimitException
        elif resp.result == 299:
            raise GroupMsgLimitException
        else:
            # todo: store msg
            return resp

    async def upload_image(self, group_id: int, file: BinaryIO) -> ImageElement:
        return await self._highway_session.upload_image(file, group_id)

    async def upload_voice(self, group_id: int, file: BinaryIO) -> VoiceElement:
        return await self._highway_session.upload_voice(file, group_id)

    async def close(self):
        """Stop Client"""
        await self.client.close()

    async def set_status(
        self,
        status: Union[int, OnlineStatus],
        battery_status: Optional[int] = None,
        is_power_connected: bool = False,
    ) -> None:
        """Change client status.

        This function wraps the :meth:`~cai.client.client.Client.register`
        method of the client.

        Args:
            status (OnlineStatus): Status want to change.
            battery_status (Optional[int], optional): Battery capacity.
                Defaults to None.
            is_power_connected (bool, optional): Is power connected to phone.
                Defaults to False.

        Raises:
            RuntimeError: Client already exists and is running.
            RuntimeError: Password not provided when login a new account.
            ApiResponseError: Invalid API request.
            RegisterException: Register Failed.
        """
        await self.client.set_status(
            status,
            battery_status,
            is_power_connected,
        )


__all__ = ["Client"]
