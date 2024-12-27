from dataclasses import dataclass
from typing import ClassVar

from pyfdec.abc.ABCFile import ABCFile
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class DoABC2(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DoABC2

    flags: int
    name: str
    ABCData: ABCFile

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'DoABC2':
        flags = buffer.read_ui32()
        name = buffer.read_string()
        ABCData = ABCFile.from_buffer(buffer.subbuffer(buffer.bytes_left()))
        return cls(flags, name, ABCData)


Tag.register(DoABC2)
