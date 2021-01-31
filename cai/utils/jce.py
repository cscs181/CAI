import struct
from typing import Optional

from jce import JceStruct, JceField, types


# com/p074qq/taf/RequestPacket.java
class RequestPacket(JceStruct):
    version: types.INT16 = JceField(0, jce_id=1)
    pkg_type: types.BYTE = JceField(bytes(1), jce_id=2)
    msg_type: types.INT32 = JceField(0, jce_id=3)
    req_id: types.INT32 = JceField(0, jce_id=4)
    servant_name: types.STRING = JceField(jce_id=5)
    func_name: types.STRING = JceField(jce_id=6)
    buffer: Optional[types.BYTES] = JceField(None, jce_id=7)
    timeout: types.INT32 = JceField(0, jce_id=8)
    context: types.MAP = JceField({}, jce_id=9)
    status: types.MAP = JceField({}, jce_id=10)


class RequestPacketVersion3(RequestPacket):
    version: types.INT16 = JceField(3, jce_id=1)
    # raw data for buffer field
    data: Optional[types.MAP[types.STRING, types.JceType]] = None

    def _prepare_buffer(self):
        if not self.data:
            raise RuntimeError("No data available")
        self.buffer = types.BYTES.validate(types.MAP.to_bytes(0, self.data))

    def encode(self, with_length: bool = False) -> bytes:
        self._prepare_buffer()
        buffer = super().encode()
        if with_length:
            return struct.pack(">I", len(buffer) + 4) + buffer
        return buffer
