from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class UploadResponse:
    uploadKey: Optional[bytes] = None
    uploadAddr: Optional[List[Tuple[str, int]]] = None
    message: Optional[str] = None
    downloadIndex: Optional[str] = None
    resourceId: Optional[int] = None
    fileId: Optional[int] = None
    fileType: Optional[int] = None
    resultCode: int = 0
    isExists: bool = False
    hasMetaData: bool = False


@dataclass
class ImageUploadResponse(UploadResponse):
    width: Optional[int] = None
    height: Optional[int] = None
