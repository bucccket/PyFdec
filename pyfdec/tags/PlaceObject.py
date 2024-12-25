from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import CxForm
from pyfdec.record_types.geometric_types import Matrix
from pyfdec.tags.Tag import Tag


@dataclass
class PlaceObject(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.PlaceObject

    characterID: int
    depth: int
    matrix: Matrix
    colorTransform: CxForm | None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        characterID = buffer.read_ui16()
        depth = buffer.read_ui16()
        matrix = Matrix.from_buffer(buffer)
        colorTransform = CxForm.from_buffer(buffer) if buffer.bytes_left() > 0 else None
        return cls(characterID, depth, matrix, colorTransform)


Tag.register(PlaceObject)
