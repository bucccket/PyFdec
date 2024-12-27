from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class DefineFontName(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineFontName

    FontID: int
    FontName: str
    FontCopyright: str

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'DefineFontName':
        FontID = buffer.read_ui16()
        FontName = buffer.read_string()
        FontCopyright = buffer.read_string()

        return cls(FontID, FontName, FontCopyright)


Tag.register(DefineFontName)
