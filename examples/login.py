"""Example Code for Login.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""
import os
import signal
import asyncio
import traceback
from io import BytesIO
from hashlib import md5

from PIL import Image

import cai
from cai.exceptions import (
    ApiResponseError, LoginException, LoginSliderNeeded, LoginCaptchaNeeded,
    LoginAccountFrozen, LoginDeviceLocked
)


async def run():
    try:
        account = os.getenv("ACCOUNT", "")
        password = os.getenv("PASSWORD")
        account = int(account)
        assert password
    except Exception:
        print(
            f"Error: account '{account}', password '{password}'"  # type: ignore
        )
        return

    try:
        client = await cai.login(account, md5(password.encode()).digest())
        print("Login Success!")
    except Exception as e:
        await handle_failure(e)


async def handle_failure(exception: Exception):
    if isinstance(exception, LoginSliderNeeded):
        print("Verify url:", exception.verify_url)
        ticket = input("Please enter the ticket: ").strip()
        try:
            await cai.submit_slider_ticket(ticket)
            print("Login Success!")
            await asyncio.sleep(3)
        except Exception as e:
            await handle_failure(e)
    elif isinstance(exception, LoginCaptchaNeeded):
        print("Captcha:")
        image = Image.open(BytesIO(exception.captcha_image))
        image.show()
        captcha = input("Please enter the captcha: ").strip()
        try:
            await cai.submit_captcha(captcha, exception.captcha_sign)
            print("Login Success!")
            await asyncio.sleep(3)
        except Exception as e:
            await handle_failure(e)
    elif isinstance(exception, LoginAccountFrozen):
        print("Account is frozen!")
    elif isinstance(exception, LoginDeviceLocked):
        print("Device lock detected!")
        way = "sms" if exception.sms_phone else "url" if exception.verify_url else ""
        if exception.sms_phone and exception.verify_url:
            while True:
                choice = input(
                    f"1. Send sms message to {exception.sms_phone}.\n"
                    f"2. Verify device by scanning.\nChoose: "
                )
                if "1" in choice:
                    way = "sms"
                    break
                elif "2" in choice:
                    way = "url"
                    break
                print(f"'{choice}' is not valid!")
        if not way:
            print("No way to verify device...")
        elif way == "sms":
            await cai.request_sms()
            print(f"SMS sent to {exception.sms_phone}!")
            sms_code = input("Please enter the sms_code: ").strip()
            try:
                await cai.submit_sms(sms_code)
            except Exception as e:
                await handle_failure(e)
        elif way == "url":
            await cai.close()
            print(f"Go to {exception.verify_url} to verify device!")
            input("Press ENTER after verification to continue login...")
            try:
                await cai.login(exception.uin)
            except Exception as e:
                await handle_failure(e)
    elif isinstance(exception, LoginException):
        print("Login Error:", repr(exception))
    elif isinstance(exception, ApiResponseError):
        print("Response Error:", repr(exception))
    else:
        print("Unknown Error:", repr(exception))
        traceback.print_exc()


if __name__ == "__main__":
    close = asyncio.Event()

    async def wait_cleanup():
        await close.wait()
        await cai.close_all()

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, close.set)
    loop.add_signal_handler(signal.SIGTERM, close.set)
    loop.create_task(run())
    loop.run_until_complete(wait_cleanup())
