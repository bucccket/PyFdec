from dataclasses import dataclass
from typing import ClassVar
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class Unknown(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.Unknown

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        return cls()


Tag.register(Unknown)
