from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class JPEGTables(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.JPEGTables

    jpegData: ExtendedBuffer

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'JPEGTables':
        jpegData = ExtendedBuffer(buffer.read())
        return cls(jpegData)


Tag.register(JPEGTables)
