import zlib
from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class DefineBitsJPEG4(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineBitsJPEG4

    characterID: int
    deblockParam: float
    imageData: ExtendedBuffer  # TODO: replace buffer with JPEG/PNG/GIF89a object
    bitmapAlphaData: ExtendedBuffer | None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'DefineBitsJPEG4':
        characterID = buffer.read_ui16()
        alphaDataOffset = buffer.read_ui32()
        deblockParam = buffer.read_fixed8()
        imageData = buffer.subbuffer(alphaDataOffset)
        jpegHeaderBytes = imageData.read(2)
        imageData.seek(0, 0)
        bitmapAlphaData = (ExtendedBuffer(zlib.decompress(buffer.read())) if jpegHeaderBytes == b'\xFF\xD8' else None)

        return cls(characterID, deblockParam, imageData, bitmapAlphaData)


Tag.register(DefineBitsJPEG4)
