from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import RGBA, CxFormWithAlpha
from pyfdec.record_types.geometric_types import Matrix
from pyfdec.tags.PlaceObject2 import PlaceObject2
from pyfdec.tags.Tag import Tag


@dataclass
class PlaceObject3(PlaceObject2):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.PlaceObject3

    @dataclass
    class Filter:

        class FilterTypes(Enum):
            DropShadowFilter = 0
            BlurFilter = 1
            GlowFilter = 2
            BevelFilter = 3
            GradientGlowFilter = 4
            ConvolutionFilter = 5
            ColorMatrixFilter = 6
            GradientBevelFilter = 7

        @dataclass
        class ColorMatrixFilter:
            matrix: list[float]

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer) -> 'PlaceObject3.Filter.ColorMatrixFilter':
                matrix = [buffer.read_f32() for _ in range(20)]
                return cls(matrix)

        @dataclass
        class ConvolutionFilter:
            matrixX: int
            matrixY: int
            divisor: float
            bias: float
            matrix: list[float]
            defaultColor: RGBA
            clamp: bool
            preserveAlpha: bool

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer) -> 'PlaceObject3.Filter.ConvolutionFilter':
                matrixX = buffer.read_ui8()
                matrixY = buffer.read_ui8()
                divisor = buffer.read_f32()
                bias = buffer.read_f32()
                matrix = [buffer.read_f32() for _ in range(matrixX * matrixY)]
                defaultColor = RGBA.from_buffer(buffer)
                with ExtendedBitIO(buffer) as bits:
                    bits.padding(6)
                    clamp = bits.read_bool()
                    preserveAlpha = bits.read_bool()
                return cls(
                    matrixX,
                    matrixY,
                    divisor,
                    bias,
                    matrix,
                    defaultColor,
                    clamp,
                    preserveAlpha,
                )

        @dataclass
        class BlurFilter:
            blurX: float
            blurY: float
            passes: int

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer) -> 'PlaceObject3.Filter.BlurFilter':
                blurX = buffer.read_fixed()
                blurY = buffer.read_fixed()
                passes = buffer.read_ui8() >> 3
                return cls(blurX, blurY, passes)

        @dataclass
        class DropShadowFilter:
            dropShadowColor: RGBA
            blurX: float
            blurY: float
            angle: float
            distance: float
            strength: float
            innerShadow: bool
            knockout: bool
            compositeSource: bool
            passes: int

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer) -> 'PlaceObject3.Filter.DropShadowFilter':
                dropShadowColor = RGBA.from_buffer(buffer)
                blurX = buffer.read_fixed()
                blurY = buffer.read_fixed()
                angle = buffer.read_fixed()
                distance = buffer.read_fixed()
                strength = buffer.read_fixed8()
                with ExtendedBitIO(buffer) as bits:
                    innerShadow = bits.read_bool()
                    knockout = bits.read_bool()
                    compositeSource = bits.read_bool()
                    passes = bits.read_unsigned(5)
                return cls(
                    dropShadowColor,
                    blurX,
                    blurY,
                    angle,
                    distance,
                    strength,
                    innerShadow,
                    knockout,
                    compositeSource,
                    passes,
                )

        @dataclass
        class GlowFilter:
            glowColor: RGBA
            blurX: float
            blurY: float
            strength: float
            innerGlow: bool
            knockout: bool
            compositeSource: bool
            passes: int

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer) -> 'PlaceObject3.Filter.GlowFilter':
                glowColor = RGBA.from_buffer(buffer)
                blurX = buffer.read_fixed()
                blurY = buffer.read_fixed()
                strength = buffer.read_fixed8()
                with ExtendedBitIO(buffer) as bits:
                    innerGlow = bits.read_bool()
                    knockout = bits.read_bool()
                    compositeSource = bits.read_bool()
                    passes = bits.read_unsigned(5)
                return cls(
                    glowColor,
                    blurX,
                    blurY,
                    strength,
                    innerGlow,
                    knockout,
                    compositeSource,
                    passes,
                )

        @dataclass
        class BevelFilter:
            shadowColor: RGBA
            highlightColor: RGBA
            blurX: float
            blurY: float
            angle: float
            distance: float
            strength: float
            innerShadow: bool
            knockout: bool
            compositeSource: bool
            onTop: bool
            passes: int

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer) -> 'PlaceObject3.Filter.BevelFilter':
                shadowColor = RGBA.from_buffer(buffer)
                highlightColor = RGBA.from_buffer(buffer)
                blurX = buffer.read_fixed()
                blurY = buffer.read_fixed()
                angle = buffer.read_fixed()
                distance = buffer.read_fixed()
                strength = buffer.read_fixed8()
                with ExtendedBitIO(buffer) as bits:
                    innerShadow = bits.read_bool()
                    knockout = bits.read_bool()
                    compositeSource = bits.read_bool()
                    onTop = bits.read_bool()
                    passes = bits.read_unsigned(4)
                return cls(
                    shadowColor,
                    highlightColor,
                    blurX,
                    blurY,
                    angle,
                    distance,
                    strength,
                    innerShadow,
                    knockout,
                    compositeSource,
                    onTop,
                    passes,
                )

        # FIXME: Idk what's up with this in the spec...
        @dataclass
        class GradientGlowFilter:
            gradientColors: list[RGBA]
            gradientRatio: list[int]
            blurX: float
            blurY: float
            angle: float
            distance: float
            strength: float
            innerShadow: bool
            knockout: bool
            compositeSource: bool
            onTop: bool
            passes: int

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer) -> 'PlaceObject3.Filter.GradientGlowFilter':
                numColors = buffer.read_ui8()
                gradientColors = [RGBA.from_buffer(buffer) for _ in range(numColors)]
                gradientRatio = [buffer.read_ui8() for _ in range(numColors)]
                blurX = buffer.read_fixed()
                blurY = buffer.read_fixed()
                angle = buffer.read_fixed()
                distance = buffer.read_fixed()
                strength = buffer.read_fixed8()
                with ExtendedBitIO(buffer) as bits:
                    innerShadow = bits.read_bool()
                    knockout = bits.read_bool()
                    compositeSource = bits.read_bool()
                    onTop = bits.read_bool()
                    passes = bits.read_unsigned(4)
                return cls(
                    gradientColors, gradientRatio, blurX, blurY, angle, distance, strength, innerShadow, knockout, compositeSource, onTop, passes
                )

        filterType: FilterTypes
        filters: ColorMatrixFilter | ConvolutionFilter | BlurFilter | DropShadowFilter | GlowFilter | BevelFilter | GradientGlowFilter

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer) -> 'PlaceObject3.Filter':
            filterType = cls.FilterTypes(buffer.read_ui8())
            match filterType:
                case cls.FilterTypes.ColorMatrixFilter:
                    filters = cls.ColorMatrixFilter.from_buffer(buffer)
                case cls.FilterTypes.ConvolutionFilter:
                    filters = cls.ConvolutionFilter.from_buffer(buffer)  # type: ignore
                case cls.FilterTypes.BlurFilter:
                    filters = cls.BlurFilter.from_buffer(buffer)  # type: ignore
                case cls.FilterTypes.DropShadowFilter:
                    filters = cls.DropShadowFilter.from_buffer(buffer)  # type: ignore
                case cls.FilterTypes.GlowFilter:
                    filters = cls.GlowFilter.from_buffer(buffer)  # type: ignore
                case cls.FilterTypes.BevelFilter:
                    filters = cls.BevelFilter.from_buffer(buffer)  # type: ignore
                case cls.FilterTypes.GradientGlowFilter:
                    filters = cls.GradientGlowFilter.from_buffer(buffer)  # type: ignore
            return cls(filterType, filters)

    class BlendModes(Enum):
        Default = 0
        Normal = 1
        Layer = 2
        Multiply = 3
        Screen = 4
        Lighten = 5
        Darken = 6
        Difference = 7
        Add = 8
        Subtract = 9
        Invert = 10
        Alpha = 11
        Erase = 12
        Overlay = 13
        HardLight = 14

    className: str | None
    surfaceFilterList: list[Filter] | None
    blendMode: BlendModes | None
    bitmapCache: bool | None
    visible: bool | None
    backgroundColor: RGBA | None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'PlaceObject3':
        with ExtendedBitIO(buffer) as bits:
            hasClipActions = bits.read_bool()
            hasClipDepth = bits.read_bool()
            hasName = bits.read_bool()
            hasRatio = bits.read_bool()
            hasColorTransform = bits.read_bool()
            hasMatrix = bits.read_bool()
            hasCharacter = bits.read_bool()
            placeFlagMove = bits.read_bool()
            bits.padding(1)
            hasOpaqueBackground = bits.read_bool()
            hasVisible = bits.read_bool()
            hasImage = bits.read_bool()
            hasClassName = bits.read_bool()
            hasCacheAsBitmap = bits.read_bool()
            hasBlendMode = bits.read_bool()
            hasFilterList = bits.read_bool()
            depth = buffer.read_ui16()
            className = (buffer.read_string() if hasClassName or (hasImage and hasCharacter) else None)
            characterID = buffer.read_ui16() if hasCharacter else None
            matrix = Matrix.from_buffer(buffer) if hasMatrix else None
            colorTransform = (CxFormWithAlpha.from_buffer(buffer) if hasColorTransform else None)
            ratio = buffer.read_ui16() if hasRatio else None
            name = buffer.read_string() if hasName else None
            clipDepth = buffer.read_ui16() if hasClipDepth else None

            surfaceFilterList = ([cls.Filter.from_buffer(buffer) for _ in range(buffer.read_ui8())] if hasFilterList else None)
            blendMode = cls.BlendModes(buffer.read_ui8()) if hasBlendMode else None
            bitmapCache = buffer.read_ui8() > 0 if hasCacheAsBitmap else None
            visible = bits.read_unsigned(8) > 0 if hasVisible else None
            backgroundColor = RGBA.from_buffer(buffer) if hasOpaqueBackground else None
            clipActions = (cls.ClipActions.from_buffer(buffer) if hasClipActions else None)

        return cls(
            characterID=characterID,  # type: ignore
            depth=depth,
            matrix=matrix,  # type: ignore
            colorTransform=colorTransform,  # type: ignore
            placeFlagMove=placeFlagMove,
            ratio=ratio,
            name=name,
            clipDepth=clipDepth,
            clipActions=clipActions,
            className=className,
            surfaceFilterList=surfaceFilterList,
            blendMode=blendMode,
            bitmapCache=bitmapCache,
            visible=visible,
            backgroundColor=backgroundColor,
        )


Tag.register(PlaceObject3)
