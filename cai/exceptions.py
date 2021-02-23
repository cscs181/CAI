"""Application Exceptions

This module is used to collect all application exceptions.

:Copyright: Copyright (C) 2021-2021  yanyongyu
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""


class CaiException(Exception):
    """Application Base Exception"""


# sso server
class SsoServerException(CaiException):
    """Server Related Exception"""


# api
class ApiException(CaiException):
    """Base Exception for API"""


class ClientNotAvailable(ApiException):
    """Cannot get client"""


class ApiResponseError(ApiException):
    """Receive a response with non zero return code."""

    def __init__(self, uin: int, seq: int, ret_code: int, command_name: str):
        self.uin = uin
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

    def __init__(self, status: int):
        self.status = status

    def __repr__(self) -> str:
        return f"LoginException(status={self.status})"


class LoginSliderException(LoginException):
    """Need Slider Ticket when Login"""

    def __init__(self, verify_url: str):
        self.verify_url = verify_url

    def __repr__(self) -> str:
        return f"LoginSliderException(verify_url={self.verify_url})"


class LoginCaptchaException(LoginException):
    """Need Captcha Image when Login"""

    def __init__(self, captcha_image: bytes, captcha_sign: bytes):
        self.captcha_image = captcha_image
        self.captcha_sign = captcha_sign

    def __repr__(self) -> str:
        return "LoginCaptchaException(captcha_image=<raw_bytes>)"
