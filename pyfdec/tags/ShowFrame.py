from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class ShowFrame(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.ShowFrame

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        return cls()


Tag.register(ShowFrame)
