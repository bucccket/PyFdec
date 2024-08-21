from dataclasses import dataclass
from typing import ClassVar
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.tags.Tag import Tag
from pyfdec.record_types.zone import ZoneRecord


@dataclass
class DefineFontAlignZones(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineFontAlignZones

    FontID: int
    CSMTableHint: int
    ZoneTable: list[ZoneRecord]

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        FontID = buffer.read_ui16()
        with ExtendedBitIO(buffer) as bits:
            CSMTableHint = bits.read_unsigned(2)
            Reserved = bits.read_unsigned(6)
            assert Reserved == 0

        ZoneTable = []
        record_buffer = buffer.subbuffer(buffer.bytes_left())
        while record_buffer.bytes_left() > 0:
            ZoneTable.append(ZoneRecord.from_buffer(record_buffer))

        return cls(
            FontID,
            CSMTableHint,
            ZoneTable
        )


Tag.register(DefineFontAlignZones)
