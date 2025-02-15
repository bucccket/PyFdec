from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class ImportAssets(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.ImportAssets

    url: str
    id_and_name: dict

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'ImportAssets':
        url = buffer.read_string()
        count = buffer.read_ui16()
        id_and_name = {}
        for _ in range(count):
            id_and_name[buffer.read_ui16()] = buffer.read_string()
        return cls(url, id_and_name)


Tag.register(ImportAssets)
