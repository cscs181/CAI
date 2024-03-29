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
    RepeatedScalarFieldContainer,
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

class MsgContentInfo(Message):
    DESCRIPTOR: Descriptor = ...
    CONTENT_INFO_ID_FIELD_NUMBER: int
    FILE_FIELD_NUMBER: int
    content_info_id: bytes = ...

    @property
    def file(self) -> MsgFile: ...

    def __init__(self,
        *,
        content_info_id : Optional[bytes] = ...,
        file : Optional[MsgFile] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"content_info_id",b"content_info_id",u"file",b"file"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"content_info_id",b"content_info_id",u"file",b"file"]) -> None: ...

class MsgFile(Message):
    DESCRIPTOR: Descriptor = ...
    BUS_ID_FIELD_NUMBER: int
    FILE_PATH_FIELD_NUMBER: int
    FILE_SIZE_FIELD_NUMBER: int
    FILE_NAME_FIELD_NUMBER: int
    DEAD_TIME_FIELD_NUMBER: int
    FILE_SHA1_FIELD_NUMBER: int
    EXT_FIELD_NUMBER: int
    FILE_MD5_FIELD_NUMBER: int
    bus_id: int = ...
    file_path: bytes = ...
    file_size: int = ...
    file_name: Text = ...
    dead_time: int = ...
    file_sha1: bytes = ...
    ext: bytes = ...
    file_md5: bytes = ...

    def __init__(self,
        *,
        bus_id : Optional[int] = ...,
        file_path : Optional[bytes] = ...,
        file_size : Optional[int] = ...,
        file_name : Optional[Text] = ...,
        dead_time : Optional[int] = ...,
        file_sha1 : Optional[bytes] = ...,
        ext : Optional[bytes] = ...,
        file_md5 : Optional[bytes] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"bus_id",b"bus_id",u"dead_time",b"dead_time",u"ext",b"ext",u"file_md5",b"file_md5",u"file_name",b"file_name",u"file_path",b"file_path",u"file_sha1",b"file_sha1",u"file_size",b"file_size"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"bus_id",b"bus_id",u"dead_time",b"dead_time",u"ext",b"ext",u"file_md5",b"file_md5",u"file_name",b"file_name",u"file_path",b"file_path",u"file_sha1",b"file_sha1",u"file_size",b"file_size"]) -> None: ...

class MsgPic(Message):
    DESCRIPTOR: Descriptor = ...
    SMALL_PIC_URL_FIELD_NUMBER: int
    ORIGINAL_PIC_URL_FIELD_NUMBER: int
    LOCAL_PIC_ID_FIELD_NUMBER: int
    small_pic_url: bytes = ...
    original_pic_url: bytes = ...
    local_pic_id: int = ...

    def __init__(self,
        *,
        small_pic_url : Optional[bytes] = ...,
        original_pic_url : Optional[bytes] = ...,
        local_pic_id : Optional[int] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"local_pic_id",b"local_pic_id",u"original_pic_url",b"original_pic_url",u"small_pic_url",b"small_pic_url"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"local_pic_id",b"local_pic_id",u"original_pic_url",b"original_pic_url",u"small_pic_url",b"small_pic_url"]) -> None: ...

class ObjMsg(Message):
    DESCRIPTOR: Descriptor = ...
    MSG_TYPE_FIELD_NUMBER: int
    TITLE_FIELD_NUMBER: int
    ABSTACT_FIELD_NUMBER: int
    TITLE_EXT_FIELD_NUMBER: int
    PIC_FIELD_NUMBER: int
    CONTENT_INFO_FIELD_NUMBER: int
    REPORT_ID_SHOW_FIELD_NUMBER: int
    msg_type: int = ...
    title: bytes = ...
    abstact: RepeatedScalarFieldContainer[bytes] = ...
    title_ext: bytes = ...
    report_id_show: int = ...

    @property
    def pic(self) -> RepeatedCompositeFieldContainer[MsgPic]: ...

    @property
    def content_info(self) -> RepeatedCompositeFieldContainer[MsgContentInfo]: ...

    def __init__(self,
        *,
        msg_type : Optional[int] = ...,
        title : Optional[bytes] = ...,
        abstact : Optional[Iterable[bytes]] = ...,
        title_ext : Optional[bytes] = ...,
        pic : Optional[Iterable[MsgPic]] = ...,
        content_info : Optional[Iterable[MsgContentInfo]] = ...,
        report_id_show : Optional[int] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"msg_type",b"msg_type",u"report_id_show",b"report_id_show",u"title",b"title",u"title_ext",b"title_ext"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"abstact",b"abstact",u"content_info",b"content_info",u"msg_type",b"msg_type",u"pic",b"pic",u"report_id_show",b"report_id_show",u"title",b"title",u"title_ext",b"title_ext"]) -> None: ...
