import lzma
import struct
import zlib
from dataclasses import dataclass
from enum import Enum
from typing import Self

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.geometric_types import Rect
from pyfdec.tags.DefineSprite import DefineSprite
from pyfdec.tags.FrameLabel import FrameLabel
from pyfdec.tags.DefineSceneAndFrameLabelData import DefineSceneAndFrameLabelData
from pyfdec.tags.DefineShape import DefineShape
from pyfdec.tags.DefineShape2 import DefineShape2
from pyfdec.tags.DefineShape3 import DefineShape3
from pyfdec.tags.DefineShape4 import DefineShape4
from pyfdec.tags.RemoveObject import RemoveObject
from pyfdec.tags.RemoveObject2 import RemoveObject2
from pyfdec.tags.StartSound import StartSound
from pyfdec.tags.StartSound2 import StartSound2
from pyfdec.tags.End import End
from pyfdec.tags.FileAttriubtes import FileAttriubtes
from pyfdec.tags.SetBackgroundColor import SetBackgroundColor
from pyfdec.tags.ShowFrame import ShowFrame
from pyfdec.tags.Tag import Tag, TagHeader


@dataclass
class SwfHeader:

    class CompressionLevel(Enum):
        NONE = b"FWS"
        ZLIB = b"CWS"
        LZMA = b"ZWS"

    compression: CompressionLevel
    version: int
    fileLength: int
    frameSize: Rect
    frameRate: float
    frameCount: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> tuple[Self, ExtendedBuffer]:
        compression = cls.CompressionLevel(buffer.read(3))
        version = buffer.read_ui8()
        fileLength = buffer.read_ui32()

        # Handle compression
        if compression == cls.CompressionLevel.ZLIB:
            file = buffer.read()

            # Decompress data
            decompressed = zlib.decompress(file)

            # Construct new buffer
            buffer = ExtendedBuffer(decompressed)
        elif compression == cls.CompressionLevel.LZMA:
            # Compressed size is never used
            _compressed_size = buffer.read_ui32()

            # Reconstruct LZMA header to work with the Python module
            size = struct.pack("<Q", fileLength - 8)
            lzmaFile = buffer.read(5) + size + buffer.read()

            # Decompress with lzma
            decompressed = lzma.decompress(lzmaFile)

            # Reconstruct header
            buffer = ExtendedBuffer(decompressed)

        frameSize = Rect.from_buffer(buffer)
        frameRate = buffer.read_fixed8()
        frameCount = buffer.read_ui16()

        return (
            cls(compression, version, fileLength, frameSize, frameRate, frameCount),
            buffer,
        )


@dataclass
class SwfFile:

    header: SwfHeader
    fileAttributes: FileAttriubtes
    tags: list[Tag]

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):

        header, buffer = SwfHeader.from_buffer(buffer)
        tags: list[Tag] = []

        while True:
            tag_header = TagHeader.from_buffer(buffer)

            tag_buffer = buffer.subbuffer(tag_header.tag_length)
            match tag_header.tag_type:
                case Tag.TagTypes.FileAttributes:
                    fileAttributes = FileAttriubtes.from_buffer(tag_buffer)
                case Tag.TagTypes.SetBackgroundColor:
                    tags.append(SetBackgroundColor.from_buffer(tag_buffer))
                case Tag.TagTypes.DefineSceneAndFrameLabelData:
                    tags.append(DefineSceneAndFrameLabelData.from_buffer(tag_buffer))
                case Tag.TagTypes.DefineShape:
                    tags.append(DefineShape.from_buffer(tag_buffer))
                case Tag.TagTypes.DefineShape2:
                    tags.append(DefineShape2.from_buffer(tag_buffer))
                case Tag.TagTypes.DefineShape3:
                    tags.append(DefineShape3.from_buffer(tag_buffer))
                case Tag.TagTypes.DefineShape4:
                    tags.append(DefineShape4.from_buffer(tag_buffer))
                case Tag.TagTypes.RemoveObject:
                    tags.append(RemoveObject.from_buffer(tag_buffer))
                case Tag.TagTypes.RemoveObject2:
                    tags.append(RemoveObject2.from_buffer(tag_buffer))
                case Tag.TagTypes.StartSound:
                    tags.append(StartSound.from_buffer(tag_buffer))
                case Tag.TagTypes.StartSound2:
                    tags.append(StartSound2.from_buffer(tag_buffer))
                case Tag.TagTypes.ShowFrame:
                    tags.append(ShowFrame.from_buffer(tag_buffer))
                case Tag.TagTypes.FrameLabel:
                    tags.append(FrameLabel.from_buffer(tag_buffer))
                case Tag.TagTypes.DefineSprite:
                    tags.append(DefineSprite.from_buffer(tag_buffer))
                case Tag.TagTypes.End:
                    tags.append(End.from_buffer(tag_buffer))
                    break
                case _:
                    raise NotImplementedError(f"Unimplemented tag type: {tag_header.tag_type}")

        # Implement check that fileAttributes is defined
        return cls(header, fileAttributes, tags)
