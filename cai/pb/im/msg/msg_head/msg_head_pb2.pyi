"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from builtins import (
    bool,
    bytes,
    int,
)

from google.protobuf.descriptor import (
    Descriptor,
    FileDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer,
)

from google.protobuf.message import (
    Message,
)

from typing import (
    Iterable,
    Optional,
    Text,
)

from typing_extensions import (
    Literal,
)


DESCRIPTOR: FileDescriptor = ...

class C2CHead(Message):
    DESCRIPTOR: Descriptor = ...
    TO_UIN_FIELD_NUMBER: int
    FROM_UIN_FIELD_NUMBER: int
    CC_TYPE_FIELD_NUMBER: int
    CC_CMD_FIELD_NUMBER: int
    AUTH_PIC_SIG_FIELD_NUMBER: int
    AUTH_SIG_FIELD_NUMBER: int
    AUTH_BUF_FIELD_NUMBER: int
    SERVER_TIME_FIELD_NUMBER: int
    CLIENT_TIME_FIELD_NUMBER: int
    RAND_FIELD_NUMBER: int
    PHONE_NUMBER_FIELD_NUMBER: int
    to_uin: int = ...
    from_uin: int = ...
    cc_type: int = ...
    cc_cmd: int = ...
    auth_pic_sig: bytes = ...
    auth_sig: bytes = ...
    auth_buf: bytes = ...
    server_time: int = ...
    client_time: int = ...
    rand: int = ...
    phone_number: Text = ...

    def __init__(self,
        *,
        to_uin : Optional[int] = ...,
        from_uin : Optional[int] = ...,
        cc_type : Optional[int] = ...,
        cc_cmd : Optional[int] = ...,
        auth_pic_sig : Optional[bytes] = ...,
        auth_sig : Optional[bytes] = ...,
        auth_buf : Optional[bytes] = ...,
        server_time : Optional[int] = ...,
        client_time : Optional[int] = ...,
        rand : Optional[int] = ...,
        phone_number : Optional[Text] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"auth_buf",b"auth_buf",u"auth_pic_sig",b"auth_pic_sig",u"auth_sig",b"auth_sig",u"cc_cmd",b"cc_cmd",u"cc_type",b"cc_type",u"client_time",b"client_time",u"from_uin",b"from_uin",u"phone_number",b"phone_number",u"rand",b"rand",u"server_time",b"server_time",u"to_uin",b"to_uin"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"auth_buf",b"auth_buf",u"auth_pic_sig",b"auth_pic_sig",u"auth_sig",b"auth_sig",u"cc_cmd",b"cc_cmd",u"cc_type",b"cc_type",u"client_time",b"client_time",u"from_uin",b"from_uin",u"phone_number",b"phone_number",u"rand",b"rand",u"server_time",b"server_time",u"to_uin",b"to_uin"]) -> None: ...

class CSHead(Message):
    DESCRIPTOR: Descriptor = ...
    UIN_FIELD_NUMBER: int
    COMMAND_FIELD_NUMBER: int
    SEQ_FIELD_NUMBER: int
    VERSION_FIELD_NUMBER: int
    RETRY_TIMES_FIELD_NUMBER: int
    CLIENT_TYPE_FIELD_NUMBER: int
    PUBNO_FIELD_NUMBER: int
    LOCALID_FIELD_NUMBER: int
    TIMEZONE_FIELD_NUMBER: int
    CLIENT_IP_FIELD_NUMBER: int
    CLIENT_PORT_FIELD_NUMBER: int
    CONN_IP_FIELD_NUMBER: int
    CONN_PORT_FIELD_NUMBER: int
    INTERFACE_IP_FIELD_NUMBER: int
    INTERFACE_PORT_FIELD_NUMBER: int
    ACTUAL_IP_FIELD_NUMBER: int
    FLAG_FIELD_NUMBER: int
    TIMESTAMP_FIELD_NUMBER: int
    SUBCMD_FIELD_NUMBER: int
    RESULT_FIELD_NUMBER: int
    APP_ID_FIELD_NUMBER: int
    INSTANCE_ID_FIELD_NUMBER: int
    SESSION_ID_FIELD_NUMBER: int
    IDC_ID_FIELD_NUMBER: int
    uin: int = ...
    command: int = ...
    seq: int = ...
    version: int = ...
    retry_times: int = ...
    client_type: int = ...
    pubno: int = ...
    localid: int = ...
    timezone: int = ...
    client_ip: int = ...
    client_port: int = ...
    conn_ip: int = ...
    conn_port: int = ...
    interface_ip: int = ...
    interface_port: int = ...
    actual_ip: int = ...
    flag: int = ...
    timestamp: int = ...
    subcmd: int = ...
    result: int = ...
    app_id: int = ...
    instance_id: int = ...
    session_id: int = ...
    idc_id: int = ...

    def __init__(self,
        *,
        uin : Optional[int] = ...,
        command : Optional[int] = ...,
        seq : Optional[int] = ...,
        version : Optional[int] = ...,
        retry_times : Optional[int] = ...,
        client_type : Optional[int] = ...,
        pubno : Optional[int] = ...,
        localid : Optional[int] = ...,
        timezone : Optional[int] = ...,
        client_ip : Optional[int] = ...,
        client_port : Optional[int] = ...,
        conn_ip : Optional[int] = ...,
        conn_port : Optional[int] = ...,
        interface_ip : Optional[int] = ...,
        interface_port : Optional[int] = ...,
        actual_ip : Optional[int] = ...,
        flag : Optional[int] = ...,
        timestamp : Optional[int] = ...,
        subcmd : Optional[int] = ...,
        result : Optional[int] = ...,
        app_id : Optional[int] = ...,
        instance_id : Optional[int] = ...,
        session_id : Optional[int] = ...,
        idc_id : Optional[int] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"actual_ip",b"actual_ip",u"app_id",b"app_id",u"client_ip",b"client_ip",u"client_port",b"client_port",u"client_type",b"client_type",u"command",b"command",u"conn_ip",b"conn_ip",u"conn_port",b"conn_port",u"flag",b"flag",u"idc_id",b"idc_id",u"instance_id",b"instance_id",u"interface_ip",b"interface_ip",u"interface_port",b"interface_port",u"localid",b"localid",u"pubno",b"pubno",u"result",b"result",u"retry_times",b"retry_times",u"seq",b"seq",u"session_id",b"session_id",u"subcmd",b"subcmd",u"timestamp",b"timestamp",u"timezone",b"timezone",u"uin",b"uin",u"version",b"version"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"actual_ip",b"actual_ip",u"app_id",b"app_id",u"client_ip",b"client_ip",u"client_port",b"client_port",u"client_type",b"client_type",u"command",b"command",u"conn_ip",b"conn_ip",u"conn_port",b"conn_port",u"flag",b"flag",u"idc_id",b"idc_id",u"instance_id",b"instance_id",u"interface_ip",b"interface_ip",u"interface_port",b"interface_port",u"localid",b"localid",u"pubno",b"pubno",u"result",b"result",u"retry_times",b"retry_times",u"seq",b"seq",u"session_id",b"session_id",u"subcmd",b"subcmd",u"timestamp",b"timestamp",u"timezone",b"timezone",u"uin",b"uin",u"version",b"version"]) -> None: ...

class DeltaHead(Message):
    DESCRIPTOR: Descriptor = ...
    TOTAL_LEN_FIELD_NUMBER: int
    OFFSET_FIELD_NUMBER: int
    ACK_OFFSET_FIELD_NUMBER: int
    COOKIE_FIELD_NUMBER: int
    ACK_COOKIE_FIELD_NUMBER: int
    RESULT_FIELD_NUMBER: int
    FLAGS_FIELD_NUMBER: int
    total_len: int = ...
    offset: int = ...
    ack_offset: int = ...
    cookie: bytes = ...
    ack_cookie: bytes = ...
    result: int = ...
    flags: int = ...

    def __init__(self,
        *,
        total_len : Optional[int] = ...,
        offset : Optional[int] = ...,
        ack_offset : Optional[int] = ...,
        cookie : Optional[bytes] = ...,
        ack_cookie : Optional[bytes] = ...,
        result : Optional[int] = ...,
        flags : Optional[int] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"ack_cookie",b"ack_cookie",u"ack_offset",b"ack_offset",u"cookie",b"cookie",u"flags",b"flags",u"offset",b"offset",u"result",b"result",u"total_len",b"total_len"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"ack_cookie",b"ack_cookie",u"ack_offset",b"ack_offset",u"cookie",b"cookie",u"flags",b"flags",u"offset",b"offset",u"result",b"result",u"total_len",b"total_len"]) -> None: ...

class Head(Message):
    DESCRIPTOR: Descriptor = ...
    HEAD_TYPE_FIELD_NUMBER: int
    CS_HEAD_FIELD_NUMBER: int
    S2C_HEAD_FIELD_NUMBER: int
    HTTPCONN_HEAD_FIELD_NUMBER: int
    PAINT_FLAG_FIELD_NUMBER: int
    LOGIN_SIG_FIELD_NUMBER: int
    DELTA_HEAD_FIELD_NUMBER: int
    C2C_HEAD_FIELD_NUMBER: int
    SCONN_HEAD_FIELD_NUMBER: int
    INST_CTRL_FIELD_NUMBER: int
    head_type: int = ...
    paint_flag: int = ...

    @property
    def cs_head(self) -> CSHead: ...

    @property
    def s2c_head(self) -> S2CHead: ...

    @property
    def httpconn_head(self) -> HttpConnHead: ...

    @property
    def login_sig(self) -> LoginSig: ...

    @property
    def delta_head(self) -> DeltaHead: ...

    @property
    def c2c_head(self) -> C2CHead: ...

    @property
    def sconn_head(self) -> SConnHead: ...

    @property
    def inst_ctrl(self) -> InstCtrl: ...

    def __init__(self,
        *,
        head_type : Optional[int] = ...,
        cs_head : Optional[CSHead] = ...,
        s2c_head : Optional[S2CHead] = ...,
        httpconn_head : Optional[HttpConnHead] = ...,
        paint_flag : Optional[int] = ...,
        login_sig : Optional[LoginSig] = ...,
        delta_head : Optional[DeltaHead] = ...,
        c2c_head : Optional[C2CHead] = ...,
        sconn_head : Optional[SConnHead] = ...,
        inst_ctrl : Optional[InstCtrl] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"c2c_head",b"c2c_head",u"cs_head",b"cs_head",u"delta_head",b"delta_head",u"head_type",b"head_type",u"httpconn_head",b"httpconn_head",u"inst_ctrl",b"inst_ctrl",u"login_sig",b"login_sig",u"paint_flag",b"paint_flag",u"s2c_head",b"s2c_head",u"sconn_head",b"sconn_head"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"c2c_head",b"c2c_head",u"cs_head",b"cs_head",u"delta_head",b"delta_head",u"head_type",b"head_type",u"httpconn_head",b"httpconn_head",u"inst_ctrl",b"inst_ctrl",u"login_sig",b"login_sig",u"paint_flag",b"paint_flag",u"s2c_head",b"s2c_head",u"sconn_head",b"sconn_head"]) -> None: ...

class HttpConnHead(Message):
    DESCRIPTOR: Descriptor = ...
    UIN_FIELD_NUMBER: int
    COMMAND_FIELD_NUMBER: int
    SUB_COMMAND_FIELD_NUMBER: int
    SEQ_FIELD_NUMBER: int
    VERSION_FIELD_NUMBER: int
    RETRY_TIMES_FIELD_NUMBER: int
    CLIENT_TYPE_FIELD_NUMBER: int
    PUB_NO_FIELD_NUMBER: int
    LOCAL_ID_FIELD_NUMBER: int
    TIME_ZONE_FIELD_NUMBER: int
    CLIENT_IP_FIELD_NUMBER: int
    CLIENT_PORT_FIELD_NUMBER: int
    QZHTTP_IP_FIELD_NUMBER: int
    QZHTTP_PORT_FIELD_NUMBER: int
    SPP_IP_FIELD_NUMBER: int
    SPP_PORT_FIELD_NUMBER: int
    FLAG_FIELD_NUMBER: int
    KEY_FIELD_NUMBER: int
    COMPRESS_TYPE_FIELD_NUMBER: int
    ORIGIN_SIZE_FIELD_NUMBER: int
    ERROR_CODE_FIELD_NUMBER: int
    REDIRECT_FIELD_NUMBER: int
    COMMAND_ID_FIELD_NUMBER: int
    SERVICE_CMDID_FIELD_NUMBER: int
    OIDBHEAD_FIELD_NUMBER: int
    uin: int = ...
    command: int = ...
    sub_command: int = ...
    seq: int = ...
    version: int = ...
    retry_times: int = ...
    client_type: int = ...
    pub_no: int = ...
    local_id: int = ...
    time_zone: int = ...
    client_ip: int = ...
    client_port: int = ...
    qzhttp_ip: int = ...
    qzhttp_port: int = ...
    spp_ip: int = ...
    spp_port: int = ...
    flag: int = ...
    key: bytes = ...
    compress_type: int = ...
    origin_size: int = ...
    error_code: int = ...
    command_id: int = ...
    service_cmdid: int = ...

    @property
    def redirect(self) -> RedirectMsg: ...

    @property
    def oidbhead(self) -> TransOidbHead: ...

    def __init__(self,
        *,
        uin : Optional[int] = ...,
        command : Optional[int] = ...,
        sub_command : Optional[int] = ...,
        seq : Optional[int] = ...,
        version : Optional[int] = ...,
        retry_times : Optional[int] = ...,
        client_type : Optional[int] = ...,
        pub_no : Optional[int] = ...,
        local_id : Optional[int] = ...,
        time_zone : Optional[int] = ...,
        client_ip : Optional[int] = ...,
        client_port : Optional[int] = ...,
        qzhttp_ip : Optional[int] = ...,
        qzhttp_port : Optional[int] = ...,
        spp_ip : Optional[int] = ...,
        spp_port : Optional[int] = ...,
        flag : Optional[int] = ...,
        key : Optional[bytes] = ...,
        compress_type : Optional[int] = ...,
        origin_size : Optional[int] = ...,
        error_code : Optional[int] = ...,
        redirect : Optional[RedirectMsg] = ...,
        command_id : Optional[int] = ...,
        service_cmdid : Optional[int] = ...,
        oidbhead : Optional[TransOidbHead] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"client_ip",b"client_ip",u"client_port",b"client_port",u"client_type",b"client_type",u"command",b"command",u"command_id",b"command_id",u"compress_type",b"compress_type",u"error_code",b"error_code",u"flag",b"flag",u"key",b"key",u"local_id",b"local_id",u"oidbhead",b"oidbhead",u"origin_size",b"origin_size",u"pub_no",b"pub_no",u"qzhttp_ip",b"qzhttp_ip",u"qzhttp_port",b"qzhttp_port",u"redirect",b"redirect",u"retry_times",b"retry_times",u"seq",b"seq",u"service_cmdid",b"service_cmdid",u"spp_ip",b"spp_ip",u"spp_port",b"spp_port",u"sub_command",b"sub_command",u"time_zone",b"time_zone",u"uin",b"uin",u"version",b"version"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"client_ip",b"client_ip",u"client_port",b"client_port",u"client_type",b"client_type",u"command",b"command",u"command_id",b"command_id",u"compress_type",b"compress_type",u"error_code",b"error_code",u"flag",b"flag",u"key",b"key",u"local_id",b"local_id",u"oidbhead",b"oidbhead",u"origin_size",b"origin_size",u"pub_no",b"pub_no",u"qzhttp_ip",b"qzhttp_ip",u"qzhttp_port",b"qzhttp_port",u"redirect",b"redirect",u"retry_times",b"retry_times",u"seq",b"seq",u"service_cmdid",b"service_cmdid",u"spp_ip",b"spp_ip",u"spp_port",b"spp_port",u"sub_command",b"sub_command",u"time_zone",b"time_zone",u"uin",b"uin",u"version",b"version"]) -> None: ...

class InstCtrl(Message):
    DESCRIPTOR: Descriptor = ...
    SEND_TO_INST_FIELD_NUMBER: int
    EXCLUDE_INST_FIELD_NUMBER: int
    FROM_INST_FIELD_NUMBER: int

    @property
    def send_to_inst(self) -> RepeatedCompositeFieldContainer[InstInfo]: ...

    @property
    def exclude_inst(self) -> RepeatedCompositeFieldContainer[InstInfo]: ...

    @property
    def from_inst(self) -> InstInfo: ...

    def __init__(self,
        *,
        send_to_inst : Optional[Iterable[InstInfo]] = ...,
        exclude_inst : Optional[Iterable[InstInfo]] = ...,
        from_inst : Optional[InstInfo] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"from_inst",b"from_inst"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"exclude_inst",b"exclude_inst",u"from_inst",b"from_inst",u"send_to_inst",b"send_to_inst"]) -> None: ...

class InstInfo(Message):
    DESCRIPTOR: Descriptor = ...
    APPPID_FIELD_NUMBER: int
    INSTID_FIELD_NUMBER: int
    PLATFORM_FIELD_NUMBER: int
    ENUM_DEVICE_TYPE_FIELD_NUMBER: int
    apppid: int = ...
    instid: int = ...
    platform: int = ...
    enum_device_type: int = ...

    def __init__(self,
        *,
        apppid : Optional[int] = ...,
        instid : Optional[int] = ...,
        platform : Optional[int] = ...,
        enum_device_type : Optional[int] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"apppid",b"apppid",u"enum_device_type",b"enum_device_type",u"instid",b"instid",u"platform",b"platform"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"apppid",b"apppid",u"enum_device_type",b"enum_device_type",u"instid",b"instid",u"platform",b"platform"]) -> None: ...

class LoginSig(Message):
    DESCRIPTOR: Descriptor = ...
    TYPE_FIELD_NUMBER: int
    SIG_FIELD_NUMBER: int
    type: int = ...
    sig: bytes = ...

    def __init__(self,
        *,
        type : Optional[int] = ...,
        sig : Optional[bytes] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"sig",b"sig",u"type",b"type"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"sig",b"sig",u"type",b"type"]) -> None: ...

class RedirectMsg(Message):
    DESCRIPTOR: Descriptor = ...
    LAST_REDIRECT_IP_FIELD_NUMBER: int
    LAST_REDIRECT_PORT_FIELD_NUMBER: int
    REDIRECT_IP_FIELD_NUMBER: int
    REDIRECT_PORT_FIELD_NUMBER: int
    REDIRECT_COUNT_FIELD_NUMBER: int
    last_redirect_ip: int = ...
    last_redirect_port: int = ...
    redirect_ip: int = ...
    redirect_port: int = ...
    redirect_count: int = ...

    def __init__(self,
        *,
        last_redirect_ip : Optional[int] = ...,
        last_redirect_port : Optional[int] = ...,
        redirect_ip : Optional[int] = ...,
        redirect_port : Optional[int] = ...,
        redirect_count : Optional[int] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"last_redirect_ip",b"last_redirect_ip",u"last_redirect_port",b"last_redirect_port",u"redirect_count",b"redirect_count",u"redirect_ip",b"redirect_ip",u"redirect_port",b"redirect_port"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"last_redirect_ip",b"last_redirect_ip",u"last_redirect_port",b"last_redirect_port",u"redirect_count",b"redirect_count",u"redirect_ip",b"redirect_ip",u"redirect_port",b"redirect_port"]) -> None: ...

class S2CHead(Message):
    DESCRIPTOR: Descriptor = ...
    SUB_MSGTYPE_FIELD_NUMBER: int
    MSG_TYPE_FIELD_NUMBER: int
    FROM_UIN_FIELD_NUMBER: int
    MSG_ID_FIELD_NUMBER: int
    RELAY_IP_FIELD_NUMBER: int
    RELAY_PORT_FIELD_NUMBER: int
    TO_UIN_FIELD_NUMBER: int
    sub_msgtype: int = ...
    msg_type: int = ...
    from_uin: int = ...
    msg_id: int = ...
    relay_ip: int = ...
    relay_port: int = ...
    to_uin: int = ...

    def __init__(self,
        *,
        sub_msgtype : Optional[int] = ...,
        msg_type : Optional[int] = ...,
        from_uin : Optional[int] = ...,
        msg_id : Optional[int] = ...,
        relay_ip : Optional[int] = ...,
        relay_port : Optional[int] = ...,
        to_uin : Optional[int] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"from_uin",b"from_uin",u"msg_id",b"msg_id",u"msg_type",b"msg_type",u"relay_ip",b"relay_ip",u"relay_port",b"relay_port",u"sub_msgtype",b"sub_msgtype",u"to_uin",b"to_uin"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"from_uin",b"from_uin",u"msg_id",b"msg_id",u"msg_type",b"msg_type",u"relay_ip",b"relay_ip",u"relay_port",b"relay_port",u"sub_msgtype",b"sub_msgtype",u"to_uin",b"to_uin"]) -> None: ...

class SConnHead(Message):
    DESCRIPTOR: Descriptor = ...

    def __init__(self,
        ) -> None: ...

class TransOidbHead(Message):
    DESCRIPTOR: Descriptor = ...
    COMMAND_FIELD_NUMBER: int
    SERVICE_TYPE_FIELD_NUMBER: int
    RESULT_FIELD_NUMBER: int
    ERROR_MSG_FIELD_NUMBER: int
    command: int = ...
    service_type: int = ...
    result: int = ...
    error_msg: Text = ...

    def __init__(self,
        *,
        command : Optional[int] = ...,
        service_type : Optional[int] = ...,
        result : Optional[int] = ...,
        error_msg : Optional[Text] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"command",b"command",u"error_msg",b"error_msg",u"result",b"result",u"service_type",b"service_type"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"command",b"command",u"error_msg",b"error_msg",u"result",b"result",u"service_type",b"service_type"]) -> None: ...
