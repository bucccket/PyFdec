from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import RGBA
from pyfdec.record_types.geometric_types import Rect
from pyfdec.tags.DefineShape3 import DefineShape3
from pyfdec.tags.Tag import Tag


@dataclass
class DefineShape4(DefineShape3):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineShape4

    @dataclass
    class ShapeWithStyle(DefineShape3.ShapeWithStyle):

        @dataclass
        class LineStyleArray(DefineShape3.ShapeWithStyle.LineStyleArray):

            @dataclass
            class LineStyle2:

                class CapStyle(Enum):
                    RoundCap = 0
                    NoCap = 1
                    SquareCap = 2

                class JoinStyle(Enum):
                    RoundJoin = 0
                    BevelJoin = 1
                    MiterJoin = 2

                width: int
                startCapStyle: CapStyle
                joinStyle: JoinStyle
                hasFillFlag: bool
                noHScaleFlag: bool
                noVScaleFlag: bool
                pixelHintingFlag: bool
                noClose: bool
                endCapStyle: CapStyle
                miterLimitFactor: int
                color: RGBA | None
                fillType: DefineShape3.ShapeWithStyle.FillStyleArray.FillStyle | None

                @classmethod
                def from_buffer(cls, buffer: ExtendedBuffer) -> 'DefineShape4.ShapeWithStyle.LineStyleArray.LineStyle2':
                    width = buffer.read_ui16()
                    with ExtendedBitIO(buffer) as bits:
                        startCapStyle = cls.CapStyle(bits.read_unsigned(2))
                        joinStyle = cls.JoinStyle(bits.read_unsigned(2))
                        hasFillFlag = bits.read_bool()
                        noHScaleFlag = bits.read_bool()
                        noVScaleFlag = bits.read_bool()
                        pixelHintingFlag = bits.read_bool()

                        # Read reserved
                        bits.read_unsigned(5)

                        noClose = bits.read_bool()
                        endCapStyle = cls.CapStyle(bits.read_unsigned(2))

                    miterLimitFactor = 0
                    if joinStyle == cls.JoinStyle.MiterJoin:
                        miterLimitFactor = buffer.read_ui16()

                    color = None
                    if not hasFillFlag:
                        color = RGBA.from_buffer(buffer=buffer)

                    fillType = None
                    if hasFillFlag:
                        fillType = DefineShape3.ShapeWithStyle.FillStyleArray.FillStyle.from_buffer(buffer)

                    return cls(
                        width=width,
                        startCapStyle=startCapStyle,
                        joinStyle=joinStyle,
                        hasFillFlag=hasFillFlag,
                        noHScaleFlag=noHScaleFlag,
                        noVScaleFlag=noVScaleFlag,
                        pixelHintingFlag=pixelHintingFlag,
                        noClose=noClose,
                        endCapStyle=endCapStyle,
                        miterLimitFactor=miterLimitFactor,
                        color=color,
                        fillType=fillType,
                    )

            lineStyles: list[LineStyle2]

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer) -> 'DefineShape4.ShapeWithStyle.LineStyleArray':
                lineStyleCount = buffer.read_ui8()

                # Read extended count
                if lineStyleCount == 0xFF:
                    lineStyleCount = buffer.read_ui16()

                lineStyles = [cls.LineStyle2.from_buffer(buffer) for _ in range(lineStyleCount)]
                return cls(lineStyles)

    shapeID: int
    shapeBounds: Rect
    edgeBounds: Rect
    usesFillWinding: bool
    usesNonScalingStrokes: bool
    usesScalingStrokes: bool
    shapes: DefineShape3.ShapeWithStyle

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'DefineShape4':
        shapeID = buffer.read_ui16()
        shapeBounds = Rect.from_buffer(buffer)
        edgeBounds = Rect.from_buffer(buffer)

        with ExtendedBitIO(buffer) as bits:
            # Read reserved
            bits.read_unsigned(5)

            usesFillWinding = bits.read_bool()
            usesNonScalingStrokes = bits.read_bool()
            usesScalingStrokes = bits.read_bool()

        shapes = cls.ShapeWithStyle.from_buffer(buffer)
        return cls(
            shapeID=shapeID,
            shapeBounds=shapeBounds,
            edgeBounds=edgeBounds,
            usesFillWinding=usesFillWinding,
            usesNonScalingStrokes=usesNonScalingStrokes,
            usesScalingStrokes=usesScalingStrokes,
            shapes=shapes,
        )


Tag.register(DefineShape4)
