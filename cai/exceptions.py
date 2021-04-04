"""Application Exceptions

This module is used to collect all application exceptions.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
from typing import Optional


class CaiException(Exception):
    """Application Base Exception"""

    def __str__(self):
        return self.__repr__()


# sso server
class SsoServerException(CaiException):
    """Server Related Exception"""


# api
class ApiException(CaiException):
    """Base Exception for API"""

    def __init__(self, uin: Optional[int]):
        self.uin = uin

    def __repr__(self) -> str:
        return f"ApiException(uin={self.uin})"


class ClientNotAvailable(ApiException):
    """Cannot get client"""

    def __init__(self, uin: Optional[int], reason: str):
        super().__init__(uin)
        self.reason = reason

    def __repr__(self) -> str:
        return f"ClientNotAvailable(uin={self.uin}, reason={self.reason})"


class ApiResponseError(ApiException):
    """Receive a response with non zero return code."""

    def __init__(self, uin: int, seq: int, ret_code: int, command_name: str):
        super().__init__(uin)
        self.seq = seq
        self.ret_code = ret_code
        self.command_name = command_name

    def __repr__(self) -> str:
        return (
            f"ApiResponseError(uin={self.uin}, seq={self.seq}, "
            f"ret_code={self.ret_code}, command_name={self.command_name})"
        )


# login api
class LoginException(ApiException):
    """Base Exception for Login"""

    def __init__(self, uin: int, status: int, message: str = ""):
        self.uin = uin
        self.status = status
        self.message = message

    def __repr__(self) -> str:
        return f"LoginException(uin={self.uin}, status={self.status}, message={self.message})"


class LoginSliderNeeded(LoginException):
    """Need Slider Ticket when Login"""

    def __init__(self, uin: int, verify_url: str):
        self.uin = uin
        self.verify_url = verify_url

    def __repr__(self) -> str:
        return f"LoginSliderException(uin={self.uin}, verify_url={self.verify_url})"


class LoginCaptchaNeeded(LoginException):
    """Need Captcha Image when Login"""

    def __init__(self, uin: int, captcha_image: bytes, captcha_sign: bytes):
        self.uin = uin
        self.captcha_image = captcha_image
        self.captcha_sign = captcha_sign

    def __repr__(self) -> str:
        return f"LoginCaptchaException(uin={self.uin}, captcha_image=<raw_bytes>)"


class LoginAccountFrozen(LoginException):
    """Account is already frozen"""

    def __init__(self, uin: int):
        self.uin = uin

    def __repr__(self) -> str:
        return "LoginAccountFrozen(uin={self.uin})"


class LoginDeviceLocked(LoginException):
    """Device lock checking is needed"""

    def __init__(
        self, uin: int, sms_phone: Optional[str], verify_url: Optional[str],
        message: Optional[str]
    ):
        self.uin = uin
        self.sms_phone = sms_phone
        self.verify_url = verify_url
        self.message = message

    def __repr__(self) -> str:
        return (
            f"LoginDeviceLocked(uin={self.uin}, message={self.message}, "
            f"sms_phone={self.sms_phone}, verify_url={self.message})"
        )


class LoginSMSRequestError(LoginException):
    """Too many sms verify request"""

    def __init__(self, uin: int):
        self.uin = uin

    def __repr__(self) -> str:
        return f"LoginSMSRequestError(uin={self.uin})"


class RegisterException(ApiException):
    """Base Exception for Login"""

    def __init__(self, uin: int, status: int, message: str = ""):
        self.uin = uin
        self.status = status
        self.message = message

    def __repr__(self) -> str:
        return f"RegisterException(uin={self.uin}, status={self.status}, message={self.message})"
