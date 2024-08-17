from dataclasses import dataclass
from typing import ClassVar
from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import RGB
from pyfdec.tags.Tag import Tag


@dataclass
class FrameLabel(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.FrameLabel

    name: str

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        name = buffer.read_string()
        anchor = buffer.readUI8()
        assert anchor == 1
        return cls(name)


Tag.register(FrameLabel)
