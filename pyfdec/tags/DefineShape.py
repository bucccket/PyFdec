from dataclasses import dataclass
from enum import Enum
from typing import ClassVar
from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import RGB
from pyfdec.record_types.geometric_types import Matrix, Rect
from pyfdec.tags.Tag import Tag


@dataclass
class DefineShape(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineShape

    @dataclass
    class ShapeWithStyle:

        @dataclass
        class FillStyle:
            @dataclass
            class Gradient:
                @dataclass
                class GradientRecord:
                    ratio: int
                    color: RGB

                    @classmethod
                    def from_buffer(cls, buffer: ExtendedBuffer):
                        return cls(
                            ratio=buffer.read_ui8(),
                            color=RGB.from_buffer(buffer)
                        )

                class SpreadMode(Enum):
                    Pad = 0
                    Reflect = 1
                    Repeat = 2

                class InterpolationMode(Enum):
                    Normal = 0
                    Linear = 1

                spreadMode: SpreadMode
                interpolationMode: InterpolationMode
                gradientRecords: list[GradientRecord]

                @classmethod
                def from_buffer(cls, buffer: ExtendedBuffer):
                    with ExtendedBitIO(buffer) as bits:
                        spreadMode = cls.SpreadMode(bits.read_unsigned(2))
                        interpolationMode = cls.InterpolationMode(
                            bits.read_unsigned(2))
                        gradientRecords = [cls.GradientRecord.from_buffer(
                            buffer) for _ in range(bits.read_unsigned(4))]
                    return cls(spreadMode, interpolationMode, gradientRecords)

            @dataclass
            class FocalGradient(Gradient):
                focalPoint: float

                @classmethod
                def from_buffer(cls, buffer: ExtendedBuffer):
                    with ExtendedBitIO(buffer) as bits:
                        spreadMode = cls.SpreadMode(bits.read_unsigned(2))
                        interpolationMode = cls.InterpolationMode(
                            bits.read_unsigned(2))
                        gradientRecords = [cls.GradientRecord.from_buffer(
                            buffer) for _ in range(bits.read_unsigned(4))]
                    focalPoint = buffer.read_fixed8()
                    return cls(spreadMode, interpolationMode, gradientRecords, focalPoint)

            class FillStyleType(Enum):
                SolidFill = 0x00
                LinearGradientFill = 0x10
                RadialGradientFill = 0x12
                FocalGradientFill = 0x13
                RepeatingBitmapFill = 0x40
                ClippedBitmapFill = 0x41
                NonSmoothedRepeatingBitmap = 0x42
                NonSmoothedClippedBitmap = 0x43

            fillStyleType: FillStyleType
            color: RGB | None = None
            gradientMatrix: tuple[Matrix, Gradient] | None = None
            bitmapMatrix: tuple[int, Matrix] | None = None

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer):
                fillStyleType = cls.FillStyleType(buffer.read_ui8())
                match(fillStyleType):
                    case fillStyleType if fillStyleType in [
                        cls.FillStyleType.SolidFill
                    ]:
                        color = RGB.from_buffer(buffer)
                        return cls(fillStyleType, color, None, None)
                    case fillStyleType if fillStyleType in [
                        cls.FillStyleType.LinearGradientFill,
                        cls.FillStyleType.RadialGradientFill,
                        cls.FillStyleType.FocalGradientFill
                    ]:
                        matrix = Matrix.from_buffer(buffer)
                        if (fillStyleType == cls.FillStyleType.LinearGradientFill
                                or fillStyleType == cls.FillStyleType.RadialGradientFill):
                            gradient = cls.Gradient.from_buffer(buffer)
                        else:
                            gradient = cls.FocalGradient.from_buffer(buffer)
                        gradientMatrix = (matrix, gradient)
                        return cls(fillStyleType, None, gradientMatrix, None)
                    case fillStyleType if fillStyleType in [
                        cls.FillStyleType.RepeatingBitmapFill,
                        cls.FillStyleType.ClippedBitmapFill,
                        cls.FillStyleType.NonSmoothedRepeatingBitmap,
                        cls.FillStyleType.NonSmoothedClippedBitmap
                    ]:
                        bitmapId = buffer.read_ui16()
                        matrix = Matrix.from_buffer(buffer)
                        bitmapMatrix = (bitmapId, matrix)
                        return cls(fillStyleType, None, None, bitmapMatrix)

        @dataclass
        class LineStyle:
            width: int
            color: RGB

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer):
                return cls(
                    width=buffer.read_ui16(),
                    color=RGB.from_buffer(buffer)
                )

        @dataclass
        class ShapeRecord:
            # note pass nbits to from_buffer
            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer, nFillBits: int, nLineBits: int):
                #TODO: continue from here
                pass
                
        fillStyles: list[FillStyle]
        lineStyles: list[LineStyle]
        shapeRecords: list[ShapeRecord]

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            fillStyleCount = buffer.read_ui8()
            if fillStyleCount == 0xFF:
                fillStyleCount = buffer.read_ui16()
            fillStyles = [cls.FillStyle.from_buffer(buffer)
                          for _ in range(fillStyleCount)]
            lineStyleCount = buffer.read_ui8()
            if lineStyleCount == 0xFF:
                lineStyleCount = buffer.read_ui16()
            lineStyles = [cls.LineStyle.from_buffer(buffer)
                          for _ in range(lineStyleCount)]
            with ExtendedBitIO(buffer) as bits:
                nFillBits = bits.read_unsigned(4)
                nLineBits = bits.read_unsigned(4)
            shapeRecords = cls.ShapeRecord.from_buffer(
                buffer, nFillBits, nLineBits)
            return cls(fillStyles, lineStyles, shapeRecords)

    shapeID: int
    shapeBounds: Rect
    shapes: ShapeWithStyle

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        shapeID = buffer.read_ui16()
        shapeBounds = Rect.from_buffer(buffer)
        shapes = cls.ShapeWithStyle.from_buffer(buffer)
        return cls(shapeID, shapeBounds, shapes)


Tag.register(DefineShape)
