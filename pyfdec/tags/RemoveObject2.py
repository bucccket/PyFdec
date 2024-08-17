from dataclasses import dataclass
from typing import ClassVar
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class RemoveObject2(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.RemoveObject2

    depth: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        depth = buffer.read_ui16()
        return cls(depth=depth)


Tag.register(RemoveObject2)