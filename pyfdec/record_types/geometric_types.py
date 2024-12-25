from dataclasses import dataclass

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class Rect:

    xmin: int
    xmax: int
    ymin: int
    ymax: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        with ExtendedBitIO(buffer) as bits:
            nbits = bits.read_unsigned(5)
            return cls(
                xmin=bits.read_signed(nbits),
                xmax=bits.read_signed(nbits),
                ymin=bits.read_signed(nbits),
                ymax=bits.read_signed(nbits),
            )


@dataclass
class Matrix:

    translate_x: float
    translate_y: float
    scale_x: float = 1.0
    scale_y: float = 1.0
    rotate_skew0: float = 1.0
    rotate_skew1: float = 1.0

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        with ExtendedBitIO(buffer) as bits:
            has_scale = bits.read_unsigned(1)
            scale_x = 1.0
            scale_y = 1.0
            if has_scale:
                nbits = bits.read_unsigned(5)
                scale_x = bits.read_fixed(nbits)
                scale_y = bits.read_fixed(nbits)
            has_rotate = bits.read_unsigned(1)
            rotate_skew0 = 1.0
            rotate_skew1 = 1.0
            if has_rotate:
                nbits = bits.read_unsigned(5)
                rotate_skew0 = bits.read_fixed(nbits)
                rotate_skew1 = bits.read_fixed(nbits)
            nbits = bits.read_unsigned(5)
            translate_x = bits.read_signed(nbits)
            translate_y = bits.read_signed(nbits)
            return cls(
                translate_x=translate_x,
                translate_y=translate_y,
                scale_x=scale_x,
                scale_y=scale_y,
                rotate_skew0=rotate_skew0,
                rotate_skew1=rotate_skew1,
            )
