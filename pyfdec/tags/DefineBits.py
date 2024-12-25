from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class DefineBits(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineBits

    characterID: int
    imageData: ExtendedBuffer  # TODO: replace buffer with JPEG object

    class FileHeaders(Enum):
        JPEG = b'\xFF\xD8'
        PNG = b'\x89PNG\x0D\x0A\x1A\x0A'
        GIF89a = b'GIF89a'

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        characterID = buffer.read_ui16()
        imageData = ExtendedBuffer(buffer.read())
        return cls(characterID, imageData)


Tag.register(DefineBits)
