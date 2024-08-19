from dataclasses import dataclass
from typing import ClassVar
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class Metadata(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.Metadata

    metadata: str

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        metadata = buffer.read_string()
        return cls(metadata)


Tag.register(Metadata)
