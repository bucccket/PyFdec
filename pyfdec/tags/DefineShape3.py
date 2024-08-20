from dataclasses import dataclass
from typing import ClassVar
from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import RGBA
from pyfdec.record_types.geometric_types import Matrix
from pyfdec.tags.Tag import Tag
from pyfdec.tags.DefineShape2 import DefineShape2


@dataclass
class DefineShape3(DefineShape2):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineShape3

    @dataclass
    class ShapeWithStyle(DefineShape2.ShapeWithStyle):
        @dataclass
        class FillStyleArray(DefineShape2.ShapeWithStyle.FillStyleArray):
            @dataclass
            class FillStyle(DefineShape2.ShapeWithStyle.FillStyleArray.FillStyle):
                @dataclass
                class Gradient(
                    DefineShape2.ShapeWithStyle.FillStyleArray.FillStyle.Gradient
                ):
                    @dataclass
                    class GradientRecord(
                        DefineShape2.ShapeWithStyle.FillStyleArray.FillStyle.Gradient.GradientRecord
                    ):
                        ratio: int
                        color: RGBA

                        @classmethod
                        def from_buffer(cls, buffer: ExtendedBuffer):
                            return cls(
                                ratio=buffer.read_ui8(), color=RGBA.from_buffer(buffer)
                            )

                # TODO: find better solution than re-implementing the class to apply overrides from Gradient
                @dataclass
                class FocalGradient(Gradient):
                    focalPoint: float

                    @classmethod
                    def from_buffer(cls, buffer: ExtendedBuffer):
                        with ExtendedBitIO(buffer) as bits:
                            spreadMode = cls.SpreadMode(bits.read_unsigned(2))
                            interpolationMode = cls.InterpolationMode(
                                bits.read_unsigned(2)
                            )
                            gradientRecords = [
                                cls.GradientRecord.from_buffer(buffer)
                                for _ in range(bits.read_unsigned(4))
                            ]
                        focalPoint = buffer.read_fixed8()
                        return cls(
                            spreadMode, interpolationMode, gradientRecords, focalPoint
                        )

                fillStyleType: (
                    DefineShape2.ShapeWithStyle.FillStyleArray.FillStyle.FillStyleType
                )
                color: RGBA | None = None
                gradientMatrix: tuple[Matrix, Gradient] | None = None
                bitmapMatrix: tuple[int, Matrix] | None = None

                @classmethod
                def from_buffer(cls, buffer: ExtendedBuffer):
                    fillStyleType = cls.FillStyleType(buffer.read_ui8())
                    match (fillStyleType):
                        case fillStyleType if fillStyleType in [
                            cls.FillStyleType.SolidFill
                        ]:
                            color = RGBA.from_buffer(buffer)
                            return cls(fillStyleType, color, None, None)
                        case fillStyleType if fillStyleType in [
                            cls.FillStyleType.LinearGradientFill,
                            cls.FillStyleType.RadialGradientFill,
                            cls.FillStyleType.FocalGradientFill,
                        ]:
                            matrix = Matrix.from_buffer(buffer)
                            if (
                                fillStyleType == cls.FillStyleType.LinearGradientFill
                                or fillStyleType == cls.FillStyleType.RadialGradientFill
                            ):
                                gradient = cls.Gradient.from_buffer(buffer)
                            else:
                                gradient = cls.FocalGradient.from_buffer(buffer)
                            gradientMatrix = (matrix, gradient)
                            return cls(fillStyleType, None, gradientMatrix, None)
                        case fillStyleType if fillStyleType in [
                            cls.FillStyleType.RepeatingBitmapFill,
                            cls.FillStyleType.ClippedBitmapFill,
                            cls.FillStyleType.NonSmoothedRepeatingBitmap,
                            cls.FillStyleType.NonSmoothedClippedBitmap,
                        ]:
                            bitmapId = buffer.read_ui16()
                            matrix = Matrix.from_buffer(buffer)
                            bitmapMatrix = (bitmapId, matrix)
                            return cls(fillStyleType, None, None, bitmapMatrix)

        @dataclass
        class LineStyleArray(DefineShape2.ShapeWithStyle.LineStyleArray):
            @dataclass
            class LineStyle(DefineShape2.ShapeWithStyle.LineStyleArray.LineStyle):
                width: int
                color: RGBA

                @classmethod
                def from_buffer(cls, buffer: ExtendedBuffer):
                    return cls(width=buffer.read_ui16(), color=RGBA.from_buffer(buffer))


Tag.register(DefineShape3)
