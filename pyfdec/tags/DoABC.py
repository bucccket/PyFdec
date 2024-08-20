from dataclasses import dataclass
from typing import ClassVar
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class DoABC(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DoABC

    ABCData: ExtendedBuffer

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        ABCData = buffer.subbuffer(buffer.bytes_left())
        return cls(ABCData)


Tag.register(DoABC)
