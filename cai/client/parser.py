from typing import Dict, Type

from .login import OICQResponse

from cai.utils.binary import Packet

# TODO: change parser type
PARSERS: Dict[str, Type[Packet]] = {"wtlogin.login": OICQResponse}
