from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class RemoveObject(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.RemoveObject

    characterId: int
    depth: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        characterId = buffer.read_ui16()
        depth = buffer.read_ui16()
        return cls(characterId=characterId, depth=depth)


Tag.register(RemoveObject)
