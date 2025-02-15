from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class EnableDebugger2(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.EnableDebugger2

    password: str

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'EnableDebugger2':
        buffer.read_ui16()  # reserved
        password = buffer.read_string()  # MD5 hash of the password
        return cls(password)


Tag.register(EnableDebugger2)
