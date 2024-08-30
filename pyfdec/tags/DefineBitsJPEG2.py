from dataclasses import dataclass
from typing import ClassVar
from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import RGB
from pyfdec.tags.DefineBits import DefineBits
from pyfdec.tags.Tag import Tag


@dataclass
class DefineBitsJPEG2(DefineBits):
    pass


Tag.register(DefineBitsJPEG2)
