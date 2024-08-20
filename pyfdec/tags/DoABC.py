from dataclasses import dataclass
from typing import ClassVar
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class DoABC(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DoABC

    flags: int
    name: str
    ABCData: ExtendedBuffer

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        flags = buffer.read_ui32()
        name = buffer.read_string()
        ABCData = buffer.subbuffer(buffer.bytes_left())
        return cls(flags, name, ABCData)


Tag.register(DoABC)
