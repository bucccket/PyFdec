from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class SetTabIndex(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.SetTabIndex

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'SetTabIndex':
        return cls()


Tag.register(SetTabIndex)
