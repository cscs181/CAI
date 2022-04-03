from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class ImageUploadResponse:
    uploadKey: Optional[bytes] = None
    uploadAddr: Optional[List[Tuple[str, int]]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    message: Optional[str] = None
    downloadIndex: Optional[str] = None
    resourceId: Optional[int] = None
    fileId: Optional[int] = None
    fileType: Optional[int] = None
    resultCode: int = 0
    isExists: bool = False
    hasMetaData: bool = False
