import zlib
from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.DefineBitsJPEG2 import DefineBitsJPEG2
from pyfdec.tags.Tag import Tag


@dataclass
class DefineBitsJPEG3(DefineBitsJPEG2):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineBitsJPEG3

    # TODO: replace buffer with JPEG/PNG/GIF89a object for image data
    bitmapAlphaData: ExtendedBuffer | None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'DefineBitsJPEG3':
        characterID = buffer.read_ui16()
        imageData = buffer.subbuffer(buffer.read_ui32())
        jpegHeaderBytes = imageData.read(2)
        imageData.seek(0, 0)
        bitmapAlphaData = (ExtendedBuffer(zlib.decompress(buffer.read())) if jpegHeaderBytes == b'\xFF\xD8' else None)

        return cls(characterID, imageData, bitmapAlphaData)


Tag.register(DefineBitsJPEG3)
