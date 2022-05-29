import struct
from cai.pb.im.oidb import OidbSsoPacket, DED3ReqBody


def build_oidb_sso_packet(cmd: int, service_type: int, body: bytes) -> bytes:
    return OidbSsoPacket(
        command=cmd,
        service_type=service_type,
        body=body
    ).SerializeToString()


# SendNudge, OidbSvc.0xed3
def build_send_nudge_pkg(target_uin: int, group: int = None, from_uin: int = None) -> bytes:
    if not (group or from_uin):
        raise ValueError("no sender")
    return build_oidb_sso_packet(
        3795, 1,
        DED3ReqBody(
            to_uin=target_uin,
            group_code=group,
            from_uin=from_uin
        ).SerializeToString()
    )


# SetAdmin, OidbSvc.0x55c_1
def build_set_admin_pkg(target_uin: int, group: int, is_admin: bool) -> bytes:
    return build_oidb_sso_packet(
        1372, 1,
        struct.pack(
            "!II?",
            group,
            target_uin,
            is_admin
        )
    )


# MuteMember, OidbSvc.0x570_8
def build_mute_member_pkg(target_uin: int, group: int, duration: int) -> bytes:
    if duration < 0:
        return ValueError("duration must be a positive value")
    return build_oidb_sso_packet(
        1392, 8,
        struct.pack(
            "!IQQQQHII",
            group,
            0, 0, 0, 0,  # 32 bytes padding
            1,
            target_uin,
            duration
        )
    )

