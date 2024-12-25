from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import RGB
from pyfdec.tags.Tag import Tag


@dataclass
class SetBackgroundColor(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.SetBackgroundColor

    backgroundColor: RGB

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        backgroundColor = RGB.from_buffer(buffer)
        return cls(backgroundColor)


Tag.register(SetBackgroundColor)
