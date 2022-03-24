"""Application Client APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

import hashlib
from typing import Union, Optional, Sequence, BinaryIO

from cai.client import OnlineStatus, Client as client_t
from cai.client.message_service.encoders import make_group_msg_pkg, build_msg
from cai.settings.device import DeviceInfo, new_device
from cai.settings.protocol import ApkInfo
from .friend import Friend as _Friend
from .group import Group as _Group
from .login import Login as _Login
from cai.utils.gcode import GroupIdConvertor
from cai.client.message_service.models import Element
from cai.client.message_service.upload import encode_d388_req
from ..client.highway import calc_file_md5_and_length, upload_image


def make_client(
    uin: int,
    passwd: Union[str, bytes],
    apk_info: ApkInfo,
    device: Optional[DeviceInfo] = None
) -> client_t:
    if not (isinstance(passwd, bytes) and len(passwd) == 16):
        # not a vailed md5 passwd
        if isinstance(passwd, bytes):
            passwd = hashlib.md5(passwd).digest()
        else:
            passwd = hashlib.md5(passwd.encode()).digest()
    if not device:
        device = new_device()
    return client_t(uin, passwd, device, apk_info)


class Client(_Login, _Friend, _Group):
    def __init__(self, client: client_t):
        self.client = client

    @property
    def connected(self) -> bool:
        return self.client.connected

    @property
    def status(self) -> Optional[OnlineStatus]:
        return self.client.status

    async def send_group_msg(self, gid: int, msg: Sequence[Element]):
        seq = self.client.next_seq()
        # todo: split long msg
        return await self.client.send_unipkg_and_wait(
            "MessageSvc.PbSendMsg",
            make_group_msg_pkg(
                seq, gid, build_msg(msg)
            ).SerializeToString()
        )

    async def upload_image(self, group_id: int, file: BinaryIO):
        return await upload_image(file, group_id, self.client)

    async def close(self):
        """Stop Client"""
        await self.client.close()

    async def set_status(
        self,
        status: Union[int, OnlineStatus],
        battery_status: Optional[int] = None,
        is_power_connected: bool = False
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
