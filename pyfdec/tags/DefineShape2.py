from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.DefineShape import DefineShape
from pyfdec.tags.Tag import Tag


@dataclass
class DefineShape2(DefineShape):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineShape2

    @dataclass
    class ShapeWithStyle(DefineShape.ShapeWithStyle):

        @dataclass
        class FillStyleArray(DefineShape.ShapeWithStyle.FillStyleArray):

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer) -> 'DefineShape2.ShapeWithStyle.FillStyleArray':
                fillStyleCount = buffer.read_ui8()

                # Read extended count
                if fillStyleCount == 0xFF:
                    fillStyleCount = buffer.read_ui16()

                fillStyles = [cls.FillStyle.from_buffer(buffer) for _ in range(fillStyleCount)]
                return cls(fillStyles)

        @dataclass
        class LineStyleArray(DefineShape.ShapeWithStyle.LineStyleArray):

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer) -> 'DefineShape2.ShapeWithStyle.LineStyleArray':
                lineStyleCount = buffer.read_ui8()

                # Read extended count
                if lineStyleCount == 0xFF:
                    lineStyleCount = buffer.read_ui16()

                lineStyles = [cls.LineStyle.from_buffer(buffer) for _ in range(lineStyleCount)]
                return cls(lineStyles)


Tag.register(DefineShape2)
