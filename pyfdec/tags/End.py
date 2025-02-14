from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class End(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.End

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'End':
        return cls()


Tag.register(End)
