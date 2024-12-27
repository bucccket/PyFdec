from dataclasses import dataclass

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ZoneRecord:

    @dataclass
    class ZoneData:
        AlignmentCoordinate: float
        Range: float

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            return cls(AlignmentCoordinate=buffer.read_f16(), Range=buffer.read_f16())

    ZoneDataList: list[ZoneData]
    ZoneMaskY: bool
    ZoneMaskX: bool

    @property
    def NumZoneData(self) -> int:
        return len(self.ZoneDataList)

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        NumZoneData = buffer.read_ui8()
        assert NumZoneData == 2
        ZoneDataList = [cls.ZoneData.from_buffer(buffer) for _ in range(NumZoneData)]
        with ExtendedBitIO(buffer) as bits:
            Reserved = bits.read_unsigned(6)
            assert Reserved == 0
            ZoneMaskY = bits.read_bool()  # yes, Y gets read first
            ZoneMaskX = bits.read_bool()

        return cls(ZoneDataList, ZoneMaskY, ZoneMaskX)
