import os
import asyncio
import traceback
from io import BytesIO
from hashlib import md5

from PIL import Image

import cai
from cai.exceptions import LoginException, LoginSliderException, LoginCaptchaException


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
        await cai.login(account, md5(password.encode()).digest())
        await asyncio.sleep(3)
    except LoginSliderException as e:
        print("Verify url:", e.verify_url)
    except LoginCaptchaException as e:
        print("Captcha:")
        image = Image.open(BytesIO(e.captcha_image))
        image.show()
    except LoginException as e:
        print("Login Error:", repr(e))
    except Exception as e:
        print("Unknown Error:", repr(e))
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run())
