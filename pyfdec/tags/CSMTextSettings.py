from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class CSMTextSettings(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.CSMTextSettings

    TextID: int
    UseFlashType: int
    GridFit: int
    Thickness: float
    Sharpness: float

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'CSMTextSettings':
        TextID = buffer.read_ui16()
        with ExtendedBitIO(buffer) as bits:
            UseFlashType = bits.read_unsigned(2)
            assert UseFlashType <= 1
            GridFit = bits.read_unsigned(3)
            Reserved = bits.read_unsigned(3)
            assert Reserved == 0

        Thickness = buffer.read_f32()
        Sharpness = buffer.read_f32()
        Reserved = buffer.read_ui8()
        assert Reserved == 0

        return cls(TextID, UseFlashType, GridFit, Thickness, Sharpness)


Tag.register(CSMTextSettings)
