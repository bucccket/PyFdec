from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import RGBA
from pyfdec.record_types.geometric_types import Rect
from pyfdec.tags.Tag import Tag


@dataclass
class DefineEditText(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineEditText

    CharacterID: int
    Bounds: Rect
    HasText: bool
    WordWrap: bool
    Multiline: bool
    Password: bool
    ReadOnly: bool
    HasTextColor: bool
    HasMaxLength: bool
    HasFont: bool
    HasFontClass: bool
    AutoSize: bool
    HasLayout: bool
    NoSelect: bool
    Border: bool
    WasStatic: bool
    Html: bool
    UseOutlines: bool
    FontID: int | None
    FontClass: str | None
    FontHeight: int | None
    TextColor: RGBA | None
    MaxLength: int | None
    Align: int | None
    LeftMargin: int | None
    RightMargin: int | None
    Indent: int | None
    Leading: int | None
    VariableName: str
    InitialText: str | None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        CharacterID = buffer.read_ui16()
        Bounds = Rect.from_buffer(buffer)
        with ExtendedBitIO(buffer) as bits:
            HasText = bits.read_bool()
            WordWrap = bits.read_bool()
            Multiline = bits.read_bool()
            Password = bits.read_bool()
            ReadOnly = bits.read_bool()
            HasTextColor = bits.read_bool()
            HasMaxLength = bits.read_bool()
            HasFont = bits.read_bool()
            HasFontClass = bits.read_bool()
            AutoSize = bits.read_bool()
            HasLayout = bits.read_bool()
            NoSelect = bits.read_bool()
            Border = bits.read_bool()
            WasStatic = bits.read_bool()
            Html = bits.read_bool()
            UseOutlines = bits.read_bool()

        FontID = buffer.read_ui16() if HasFont else None
        FontClass = buffer.read_string() if HasFontClass else None
        FontHeight = buffer.read_ui16() if HasFont else None
        TextColor = RGBA.from_buffer(buffer) if HasTextColor else None
        MaxLength = buffer.read_ui16() if HasMaxLength else None
        Align, LeftMargin, RightMargin, Indent, Leading = \
            (buffer.read_ui8(), buffer.read_ui16(), buffer.read_ui16(), buffer.read_ui16(), buffer.read_si16()) \
            if HasLayout else (None, None, None, None, None)

        VariableName = buffer.read_string()
        InitialText = buffer.read_string() if HasText else None
        return cls(
            CharacterID, Bounds, HasText, WordWrap, Multiline, Password, ReadOnly, HasTextColor, HasMaxLength, HasFont,
            HasFontClass, AutoSize, HasLayout, NoSelect, Border, WasStatic, Html, UseOutlines, FontID, FontClass,
            FontHeight, TextColor, MaxLength, Align, LeftMargin, RightMargin, Indent, Leading, VariableName, InitialText
        )


Tag.register(DefineEditText)
