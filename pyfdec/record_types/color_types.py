from dataclasses import dataclass

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class RGB:
    red: int = 0
    green: int = 0
    blue: int = 0

    def toHexString(self) -> str:
        return '#%02x%02x%02x' % (self.red, self.green, self.blue)

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'RGB':
        return cls(red=buffer.read_ui8(), green=buffer.read_ui8(), blue=buffer.read_ui8())


@dataclass
class RGBA(RGB):
    alpha: int = 0

    def toHexString(self) -> str:
        return '#%02x%02x%02x' % (self.red, self.green, self.blue)

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'RGBA':
        return cls(
            red=buffer.read_ui8(),
            green=buffer.read_ui8(),
            blue=buffer.read_ui8(),
            alpha=buffer.read_ui8(),
        )


@dataclass
class ARGB:
    alpha: int = 0
    red: int = 0
    green: int = 0
    blue: int = 0

    def toHexString(self) -> str:
        return '#%02x%02x%02x' % (self.red, self.green, self.blue)

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'ARGB':
        return cls(
            alpha=buffer.read_ui8(),
            red=buffer.read_ui8(),
            green=buffer.read_ui8(),
            blue=buffer.read_ui8(),
        )


@dataclass
class CxForm:
    RedMultTerm: int = 1
    GreenMultTerm: int = 1
    BlueMultTerm: int = 1
    RedAddTerm: int = 1
    GreenAddTerm: int = 1
    BlueAddTerm: int = 1

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'CxForm':
        with ExtendedBitIO(buffer) as bits:
            has_add_terms = bits.read_bool()
            has_mult_terms = bits.read_bool()
            red_mult_term = 1
            green_mult_term = 1
            blue_mult_term = 1
            red_add_term = 1
            green_add_term = 1
            blue_add_term = 1
            nbits = bits.read_unsigned(4)
            if has_mult_terms:
                red_mult_term = bits.read_signed(nbits)
                green_mult_term = bits.read_signed(nbits)
                blue_mult_term = bits.read_signed(nbits)
            if has_add_terms:
                red_add_term = bits.read_signed(nbits)
                green_add_term = bits.read_signed(nbits)
                blue_add_term = bits.read_signed(nbits)
            return cls(
                RedMultTerm=red_mult_term,
                GreenMultTerm=green_mult_term,
                BlueMultTerm=blue_mult_term,
                RedAddTerm=red_add_term,
                GreenAddTerm=green_add_term,
                BlueAddTerm=blue_add_term,
            )


@dataclass
class CxFormWithAlpha:
    RedMultTerm: int = 1
    GreenMultTerm: int = 1
    BlueMultTerm: int = 1
    AlphaMultTerm: int = 1
    RedAddTerm: int = 1
    GreenAddTerm: int = 1
    BlueAddTerm: int = 1
    AlphaAddTerm: int = 1

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'CxFormWithAlpha':
        with ExtendedBitIO(buffer) as bits:
            has_add_terms = bits.read_bool()
            has_mult_terms = bits.read_bool()
            red_mult_term = 1
            green_mult_term = 1
            blue_mult_term = 1
            alpha_mult_term = 1
            red_add_term = 1
            green_add_term = 1
            blue_add_term = 1
            alpha_add_term = 1
            nbits = bits.read_unsigned(4)
            if has_mult_terms:
                red_mult_term = bits.read_signed(nbits)
                green_mult_term = bits.read_signed(nbits)
                blue_mult_term = bits.read_signed(nbits)
                alpha_mult_term = bits.read_signed(nbits)
            if has_add_terms:
                red_add_term = bits.read_signed(nbits)
                green_add_term = bits.read_signed(nbits)
                blue_add_term = bits.read_signed(nbits)
                alpha_add_term = bits.read_signed(nbits)
            return cls(
                RedMultTerm=red_mult_term,
                GreenMultTerm=green_mult_term,
                BlueMultTerm=blue_mult_term,
                AlphaMultTerm=alpha_mult_term,
                RedAddTerm=red_add_term,
                GreenAddTerm=green_add_term,
                BlueAddTerm=blue_add_term,
                AlphaAddTerm=alpha_add_term,
            )
