from dataclasses import dataclass
from enum import Enum

from pyfdec.record_types.geometric_types import Rect


@dataclass
class SwfHeader:
    
    class CompressionLevel(Enum):
        Uncompressed = b'FWS'
        Zlib = b'CWS'
        LZMA = b'ZWS'

    compression: CompressionLevel
    version: int
    fileLength: int
    frameSize: Rect
    frameRate: float
    frameCount: int
    
    @classmethod
    def from_buffer(cls, buffer):
        compression = cls.CompressionLevel(buffer.read(3))
        version = buffer.read_ui8()
        fileLength = buffer.read_ui32()
        frameSize = Rect.from_buffer(buffer)
        frameRate = buffer.read_fixed8()
        frameCount = buffer.read_ui16()
        return cls(compression, version, fileLength, frameSize, frameRate, frameCount)


@dataclass
class SwfFile:
    
    header: SwfHeader
    fileAttributes: Any
    tags: list[Any]
    
    @classmethod
    def from_buffer(cls, buffer):
        pass