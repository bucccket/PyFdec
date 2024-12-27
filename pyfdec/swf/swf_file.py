import lzma
import struct
import zlib
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generator

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.geometric_types import Rect
from pyfdec.tags.CSMTextSettings import CSMTextSettings
from pyfdec.tags.DefineBits import DefineBits
from pyfdec.tags.DefineBitsJPEG2 import DefineBitsJPEG2
from pyfdec.tags.DefineBitsJPEG3 import DefineBitsJPEG3
from pyfdec.tags.DefineBitsJPEG4 import DefineBitsJPEG4
from pyfdec.tags.DefineEditText import DefineEditText
from pyfdec.tags.DefineFontAlignZones import DefineFontAlignZones
from pyfdec.tags.DefineFontName import DefineFontName
from pyfdec.tags.DefineSceneAndFrameLabelData import DefineSceneAndFrameLabelData
from pyfdec.tags.DefineShape import DefineShape
from pyfdec.tags.DefineShape2 import DefineShape2
from pyfdec.tags.DefineShape3 import DefineShape3
from pyfdec.tags.DefineShape4 import DefineShape4
from pyfdec.tags.DefineSprite import DefineSprite
from pyfdec.tags.DoABC import DoABC
from pyfdec.tags.DoABC2 import DoABC2
from pyfdec.tags.End import End
from pyfdec.tags.FileAttributes import FileAttributes
from pyfdec.tags.FrameLabel import FrameLabel
from pyfdec.tags.JPEGTables import JPEGTables
from pyfdec.tags.Metadata import Metadata
from pyfdec.tags.PlaceObject import PlaceObject
from pyfdec.tags.PlaceObject2 import PlaceObject2
from pyfdec.tags.PlaceObject3 import PlaceObject3
from pyfdec.tags.RemoveObject import RemoveObject
from pyfdec.tags.RemoveObject2 import RemoveObject2
from pyfdec.tags.ScriptLimits import ScriptLimits
from pyfdec.tags.SetBackgroundColor import SetBackgroundColor
from pyfdec.tags.ShowFrame import ShowFrame
from pyfdec.tags.StartSound import StartSound
from pyfdec.tags.StartSound2 import StartSound2
from pyfdec.tags.SymbolClass import SymbolClass
from pyfdec.tags.Tag import Tag, TagHeader
from pyfdec.tags.Unknown import Unknown


@dataclass
class SwfHeader:

    class CompressionLevel(Enum):
        NONE = b'FWS'
        ZLIB = b'CWS'
        LZMA = b'ZWS'

    compression: CompressionLevel
    version: int
    fileLength: int
    frameSize: Rect
    frameRate: float
    frameCount: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> tuple['SwfHeader', ExtendedBuffer]:
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
            _compressed_size = buffer.read_ui32()  # noqa: F841

            # Reconstruct LZMA header to work with the Python module
            size = struct.pack('<Q', fileLength - 8)
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
    fileAttributes: FileAttributes
    tags: Generator[Tag, Any, None]

    @staticmethod
    def get_tag_list(buffer: ExtendedBuffer):
        while True:
            tag_header = TagHeader.from_buffer(buffer)

            tag_buffer = buffer.subbuffer(tag_header.tag_length)
            match tag_header.tag_type:
                case Tag.TagTypes.FileAttributes:
                    yield FileAttributes.from_buffer(tag_buffer)
                case Tag.TagTypes.SetBackgroundColor:
                    yield SetBackgroundColor.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineSceneAndFrameLabelData:
                    yield DefineSceneAndFrameLabelData.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineEditText:
                    yield DefineEditText.from_buffer(tag_buffer)
                case Tag.TagTypes.CSMTextSettings:
                    yield CSMTextSettings.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineFontAlignZones:
                    yield DefineFontAlignZones.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineFontName:
                    yield DefineFontName.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineShape:
                    yield DefineShape.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineShape2:
                    yield DefineShape2.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineShape3:
                    yield DefineShape3.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineShape4:
                    yield DefineShape4.from_buffer(tag_buffer)
                case Tag.TagTypes.RemoveObject:
                    yield RemoveObject.from_buffer(tag_buffer)
                case Tag.TagTypes.RemoveObject2:
                    yield RemoveObject2.from_buffer(tag_buffer)
                case Tag.TagTypes.StartSound:
                    yield StartSound.from_buffer(tag_buffer)
                case Tag.TagTypes.StartSound2:
                    yield StartSound2.from_buffer(tag_buffer)
                case Tag.TagTypes.ShowFrame:
                    yield ShowFrame.from_buffer(tag_buffer)
                case Tag.TagTypes.FrameLabel:
                    yield FrameLabel.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineSprite:
                    yield DefineSprite.from_buffer(tag_buffer)
                case Tag.TagTypes.PlaceObject:
                    yield PlaceObject.from_buffer(tag_buffer)
                case Tag.TagTypes.PlaceObject2:
                    yield PlaceObject2.from_buffer(tag_buffer)
                case Tag.TagTypes.PlaceObject3:
                    yield PlaceObject3.from_buffer(tag_buffer)
                case Tag.TagTypes.Metadata:
                    yield Metadata.from_buffer(tag_buffer)
                case Tag.TagTypes.ScriptLimits:
                    yield ScriptLimits.from_buffer(tag_buffer)
                case Tag.TagTypes.SymbolClass:
                    yield SymbolClass.from_buffer(tag_buffer)
                case Tag.TagTypes.DoABC:
                    yield DoABC.from_buffer(tag_buffer)
                case Tag.TagTypes.DoABC2:
                    yield DoABC2.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineBits:
                    yield DefineBits.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineBitsJPEG2:
                    yield DefineBitsJPEG2.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineBitsJPEG3:
                    yield DefineBitsJPEG3.from_buffer(tag_buffer)
                case Tag.TagTypes.DefineBitsJPEG4:
                    yield DefineBitsJPEG4.from_buffer(tag_buffer)
                case Tag.TagTypes.JPEGTables:
                    yield JPEGTables.from_buffer(tag_buffer)
                case Tag.TagTypes.Unknown:
                    yield Unknown.from_buffer(tag_buffer)
                case Tag.TagTypes.End:
                    yield End.from_buffer(tag_buffer)
                    break
                case _:
                    raise NotImplementedError(f'Unimplemented tag: {tag_header.tag_type}')

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):

        header, buffer = SwfHeader.from_buffer(buffer)

        tag_header = TagHeader.from_buffer(buffer)
        tag_buffer = buffer.subbuffer(tag_header.tag_length)
        fileAttributes: FileAttributes = FileAttributes.from_buffer(tag_buffer)

        tags: Generator[Tag, Any, None] = cls.get_tag_list(buffer)

        # Implement check that fileAttributes is defined
        return cls(header, fileAttributes, tags)
