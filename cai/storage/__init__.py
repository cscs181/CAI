import os
import shutil

from .utils import user_config_dir, user_cache_dir


class Storage:
    app_name: str = "CAI"

    default_app_dir: str = user_config_dir(app_name, roaming=True)
    app_dir: str = os.getenv(f"{app_name}_APP_DIR", default_app_dir)
    if not os.path.exists(app_dir):
        os.mkdir(app_dir)
    if not os.path.isdir(app_dir):
        raise RuntimeError(
            f"Application directory {app_dir} is not a directory!")

    default_cache_dir: str = user_cache_dir(app_name)
    cache_dir: str = os.getenv(f"{app_name}_CACHE_DIR", default_cache_dir)
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    if not os.path.isdir(cache_dir):
        raise RuntimeError(
            f"Application Cache directory {cache_dir} is not a directory!")

    device_file: str = os.path.join(app_dir, "device.json")

    @classmethod
    def clear_cache(cls):
        for path in os.listdir(cls.cache_dir):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
