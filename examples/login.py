import os
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
        await asyncio.sleep(3)
    except Exception as e:
        await handle_failure(e)
    finally:
        await cai.close()


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
    elif isinstance(exception, LoginException):
        print("Login Error:", repr(exception))
    elif isinstance(exception, ApiResponseError):
        print("Response Error:", repr(exception))
    else:
        print("Unknown Error:", repr(exception))
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run())
