"""Connection Related tools

This module is used to build tcp latency test and other convenient tools.

Copyright (C) 2021-2021  yanyongyu

License AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/yanyongyu/CAI/blob/master/LICENSE
"""
import time
import math

from . import connect


async def tcp_latency_test(host: str, port: int, timeout: float = 5.) -> float:
    start = time.time()

    try:
        async with connect(host, port, timeout=timeout):
            pass
    except ConnectionError:
        return math.inf

    end = time.time()
    return (end - start) * 1000
