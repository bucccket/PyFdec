from dataclasses import dataclass
from enum import Enum
from typing import Any, ClassVar, Generator
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
        class FillStyleArray:
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
                                ratio=buffer.read_ui8(), color=RGB.from_buffer(buffer)
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
                                bits.read_unsigned(2)
                            )
                            gradientRecords = [
                                cls.GradientRecord.from_buffer(buffer)
                                for _ in range(bits.read_unsigned(4))
                            ]
                        return cls(spreadMode, interpolationMode, gradientRecords)

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
                    match (fillStyleType):
                        case fillStyleType if fillStyleType in [
                            cls.FillStyleType.SolidFill
                        ]:
                            color = RGB.from_buffer(buffer)
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

            fillStyles: list[FillStyle]

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer):
                fillStyleCount = buffer.read_ui8()
                fillStyles = [
                    cls.FillStyle.from_buffer(buffer) for _ in range(fillStyleCount)
                ]
                return cls(fillStyles)

        @dataclass
        class LineStyleArray:
            @dataclass
            class LineStyle:
                width: int
                color: RGB

                @classmethod
                def from_buffer(cls, buffer: ExtendedBuffer):
                    return cls(width=buffer.read_ui16(), color=RGB.from_buffer(buffer))

            lineStyles: list[LineStyle]

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer):
                lineStyleCount = buffer.read_ui8()
                lineStyles = [
                    cls.LineStyle.from_buffer(buffer) for _ in range(lineStyleCount)
                ]
                return cls(lineStyles)

        @dataclass
        class ShapeRecord:
            pass

        @dataclass
        class EndShapeRecord(ShapeRecord):
            pass

        # NOTE: Technically python allows to define class members very loosely
        # It would be nice to make use of it and not blindly stick to dataclasses
        # They overstay their welcome
        @dataclass
        class StyleChangeRecord(ShapeRecord):
            moveDeltaX: int | None = None
            moveDeltaY: int | None = None
            fillStyle0: int | None = None
            fillStyle1: int | None = None
            lineStyle: int | None = None
            newFillStyleArray: Any | None = None
            newLineStyleArray: Any | None = None

        @dataclass
        class StraightEdgeRecord(ShapeRecord):
            deltaX: int = 0
            deltaY: int = 0

        @dataclass
        class CurvedEdgeRecord(ShapeRecord):
            controlDeltaX: int = 0
            controlDeltaY: int = 0
            anchorDeltaX: int = 0
            anchorDeltaY: int = 0

        fillStyleArray: FillStyleArray
        lineStyleArray: LineStyleArray
        shapeRecords: Generator[ShapeRecord, Any, None]

        @classmethod
        def _read_shape_records(cls, buffer: ExtendedBuffer):
            with ExtendedBitIO(buffer) as bits:
                fillBits = bits.read_unsigned(4)
                lineBits = bits.read_unsigned(4)

                while True:
                    typeFlag = bits.read_bool()
                    if not typeFlag:
                        stateNewStyles = bits.read_bool()
                        stateLineStyle = bits.read_bool()
                        stateFillStyle1 = bits.read_bool()
                        stateFillStyle0 = bits.read_bool()
                        stateMoveTo = bits.read_bool()
                        if (
                            stateNewStyles
                            or stateLineStyle
                            or stateFillStyle1
                            or stateFillStyle0
                            or stateMoveTo
                        ):
                            # StyleChangeRecord
                            moveDeltaX = None
                            moveDeltaY = None
                            fillStyle0 = None
                            fillStyle1 = None
                            lineStyle = None
                            newFillStyleArray = None
                            newLineStyleArray = None
                            if stateMoveTo:
                                moveBits = bits.read_unsigned(5)
                                moveDeltaX = bits.read_signed(moveBits)
                                moveDeltaY = bits.read_signed(moveBits)
                            if stateFillStyle0:
                                fillStyle0 = bits.read_unsigned(fillBits)
                            if stateFillStyle1:
                                fillStyle1 = bits.read_unsigned(fillBits)
                            if stateLineStyle:
                                lineStyle = bits.read_unsigned(lineBits)
                            if stateNewStyles:
                                bits.align()
                                newFillStyleArray = cls.FillStyleArray.from_buffer(
                                    buffer
                                )
                                newLineStyleArray = cls.LineStyleArray.from_buffer(
                                    buffer
                                )
                                fillBits = bits.read_unsigned(4)
                                lineBits = bits.read_unsigned(4)
                            yield cls.StyleChangeRecord(
                                moveDeltaX=moveDeltaX,
                                moveDeltaY=moveDeltaY,
                                fillStyle0=fillStyle0,
                                fillStyle1=fillStyle1,
                                lineStyle=lineStyle,
                                newFillStyleArray=newFillStyleArray,
                                newLineStyleArray=newLineStyleArray,
                            )
                        else:
                            # EndShapeRecord
                            yield cls.EndShapeRecord()
                            break
                    else:
                        # EdgeRecord
                        straightFlag = bits.read_bool()
                        if straightFlag:
                            nBits = bits.read_unsigned(4)
                            generalLine = bits.read_bool()
                            verticalLine = True
                            horizontalLine = True
                            deltaX = 0
                            deltaY = 0
                            if not generalLine:
                                verticalLine = bits.read_bool()
                                horizontalLine = not verticalLine
                            if horizontalLine:
                                deltaX = bits.read_signed(nBits + 2)
                            if verticalLine:
                                deltaY = bits.read_signed(nBits + 2)
                            yield cls.StraightEdgeRecord(deltaX, deltaY)
                        else:
                            nBits = bits.read_unsigned(4)
                            controlDeltaX = bits.read_signed(nBits + 2)
                            controlDeltaY = bits.read_signed(nBits + 2)
                            anchorDeltaX = bits.read_signed(nBits + 2)
                            anchorDeltaY = bits.read_signed(nBits + 2)
                            yield cls.CurvedEdgeRecord(
                                controlDeltaX,
                                controlDeltaY,
                                anchorDeltaX,
                                anchorDeltaY,
                            )

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            fillStyleArray = cls.FillStyleArray.from_buffer(buffer)
            lineStyleArray = cls.LineStyleArray.from_buffer(buffer)
            shapeRecords = cls._read_shape_records(buffer)
            return cls(fillStyleArray, lineStyleArray, shapeRecords)

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
