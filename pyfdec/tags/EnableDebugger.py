from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class EnableDebugger(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.EnableDebugger

    password: str

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'EnableDebugger':
        password = buffer.read_string()  # MD5 hash of the password
        return cls(password)


Tag.register(EnableDebugger)
