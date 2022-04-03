"""Application Login APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
from .base import BaseAPI
from cai.exceptions import LoginException


class Login(BaseAPI):
    async def login(self):
        """Create a new client (or use an existing one) and login.

        This function wraps the :meth:`~cai.client.client.Client.login` method of the client.

        Raises:
            LoginSliderException: Need slider ticket.
            LoginCaptchaException: Need captcha image.
        """
        await self.client.connect()
        try:
            await self._executor("login")
        except LoginException:
            raise  # user handle required
        except Exception:
            await self.client.close()
            raise

    async def submit_captcha(
        self, captcha: str, captcha_sign: bytes
    ) -> bool:
        """Submit captcha data to login.

        This function wraps the :meth:`~cai.client.client.Client.submit_captcha`
        method of the client.

        Args:
            captcha (str): Captcha data to submit.
            captcha_sign (bytes): Captcha sign received when login.

        Raises:
            LoginSliderException: Need slider ticket.
            LoginCaptchaException: Need captcha image.
        """
        try:
            await self._executor("submit_captcha", captcha, captcha_sign)
        except not LoginException:
            await self.client.close()
            raise
        return True

    async def submit_slider_ticket(self, ticket: str) -> bool:
        """Submit slider ticket to login.

        This function wraps the :meth:`~cai.client.client.Client.submit_slider_ticket`
        method of the client.

        Args:
            ticket (str): Slider ticket to submit.

        Raises:
            LoginSliderException: Need slider ticket.
            LoginCaptchaException: Need captcha image.
        """
        await self._executor("submit_slider_ticket", ticket)
        return True

    async def request_sms(self) -> bool:
        """Request sms code message to login.

        This function wraps the :meth:`~cai.client.client.Client.request_sms`
        method of the client.

        Args:
            uin (Optional[int], optional): Account of the client want to login.
                Defaults to None.

        Raises:
            LoginSMSRequestError: Too many SMS messages were sent.
        """
        try:
            return await self.client.request_sms()
        except not LoginException:
            await self.client.close()
            raise

    async def submit_sms(self, sms_code: str) -> bool:
        """Submit sms code to login.

        This function wraps the :meth:`~cai.client.client.Client.submit_sms`
        method of the client.

        Args:
            sms_code (str): SMS code to submit.

        Raises:
            LoginSliderException: Need slider ticket.
            LoginCaptchaException: Need captcha image.
        """
        try:
            await self._executor("submit_sms", sms_code)
        except not LoginException:
            await self.client.close()
            raise
        return True


__all__ = [
    "Login"
]
