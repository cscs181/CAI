from jce import JceStruct, JceField, types

from cai.connection import connect
from cai.settings.protocol import get_protocol


# com/tencent/msf/service/protocol/serverconfig/C32504d.java
# renamed from: com.tencent.msf.service.protocol.serverconfig.d
class SsoServerRequest(JceStruct):
    f172840a: types.INT64 = JceField(jce_id=1)
    f172841b: types.INT64 = JceField(jce_id=2)
    f172842c: types.BYTE = JceField(jce_id=3)
    f172843d: types.STRING = JceField(jce_id=4)
    f172844e: types.INT32 = JceField(jce_id=5)
    f172845f: types.INT64 = JceField(jce_id=6)
    f172846g: types.STRING = JceField(jce_id=7)
    f172847h: types.INT64 = JceField(jce_id=8)
    f172848i: types.INT64 = JceField(jce_id=9)
    f172849j: types.INT64 = JceField(jce_id=10)
    f172850k: types.BYTE = JceField(jce_id=11)
    f172851l: types.BYTE = JceField(jce_id=12)
    f172852m: types.INT64 = JceField(jce_id=13)


# com/tencent/mobileqq/msf/core/p205a/C25979f.java
def get_sso_address():
    protocol = get_protocol()
    key = bytes(
        [
            0xF0, 0x44, 0x1F, 0x5F, 0xF4, 0x2D, 0xA5, 0x8F, 0xDC, 0xF7, 0x94,
            0x9A, 0xBA, 0x62, 0xD4, 0x11
        ]
    )
