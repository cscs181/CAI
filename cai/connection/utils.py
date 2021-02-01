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
