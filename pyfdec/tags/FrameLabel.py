from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class FrameLabel(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.FrameLabel

    name: str
    anchor: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        name = buffer.read_string()
        anchor = buffer.read_ui8()
        return cls(name, anchor)


Tag.register(FrameLabel)
