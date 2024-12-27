from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class ScriptLimits(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.ScriptLimits

    max_recursion_depth: int
    script_timeout_seconds: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'ScriptLimits':
        max_recursion_depth = buffer.read_ui16()
        script_timeout_seconds = buffer.read_ui16()
        return cls(max_recursion_depth, script_timeout_seconds)


Tag.register(ScriptLimits)
