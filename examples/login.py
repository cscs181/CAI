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
        await client.close()
    except LoginSliderNeeded as e:
        print("Verify url:", e.verify_url)
    except LoginCaptchaNeeded as e:
        print("Captcha:")
        image = Image.open(BytesIO(e.captcha_image))
        image.show()
    except LoginAccountFrozen as e:
        print("Account is frozen!")
    except LoginDeviceLocked as e:
        print("Device lock detected!")
    except LoginException as e:
        print("Login Error:", repr(e))
    except ApiResponseError as e:
        print("Response Error:", repr(e))
    except Exception as e:
        print("Unknown Error:", repr(e))
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run())
