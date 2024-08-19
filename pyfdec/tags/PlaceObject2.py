from dataclasses import dataclass
from typing import Any, ClassVar

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import RGB, CxForm, CxFormWithAlpha
from pyfdec.record_types.geometric_types import Matrix
from pyfdec.tags.PlaceObject import PlaceObject
from pyfdec.tags.Tag import Tag


@dataclass
class PlaceObject2(PlaceObject):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.PlaceObject2

    @dataclass
    class ClipActions:
        @dataclass
        class ClipEventFlags:
            clipEventKeyUp: bool
            clipEventKeyDown: bool
            clipEventMouseUp: bool
            clipEventMouseDown: bool
            clipEventMouseMove: bool
            clipEventUnload: bool
            clipEventEnterFrame: bool
            clipEventLoad: bool
            clipEventDragOver: bool
            clipEventRollOut: bool
            clipEventRollOver: bool
            clipEventReleaseOutside: bool
            clipEventRelease: bool
            clipEventPress: bool
            clipEventInitialize: bool
            clipEventData: bool
            clipEventConstruct: bool
            clipEventKeyPress: bool
            clipEventDragOut: bool

            def getEventCount(self):
                return sum(
                    [
                        self.clipEventKeyUp,
                        self.clipEventKeyDown,
                        self.clipEventMouseUp,
                        self.clipEventMouseDown,
                        self.clipEventMouseMove,
                        self.clipEventUnload,
                        self.clipEventEnterFrame,
                        self.clipEventLoad,
                        self.clipEventDragOver,
                        self.clipEventRollOut,
                        self.clipEventRollOver,
                        self.clipEventReleaseOutside,
                        self.clipEventRelease,
                        self.clipEventPress,
                        self.clipEventInitialize,
                        self.clipEventData,
                        self.clipEventConstruct,
                        self.clipEventKeyPress,
                        self.clipEventDragOut,
                    ]
                )

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer):
                with ExtendedBitIO(buffer) as bits:
                    clipEventKeyUp = bits.read_bool()
                    clipEventKeyDown = bits.read_bool()
                    clipEventMouseUp = bits.read_bool()
                    clipEventMouseDown = bits.read_bool()
                    clipEventMouseMove = bits.read_bool()
                    clipEventUnload = bits.read_bool()
                    clipEventEnterFrame = bits.read_bool()
                    clipEventLoad = bits.read_bool()
                    clipEventDragOver = bits.read_bool()
                    clipEventRollOut = bits.read_bool()
                    clipEventRollOver = bits.read_bool()
                    clipEventReleaseOutside = bits.read_bool()
                    clipEventRelease = bits.read_bool()
                    clipEventPress = bits.read_bool()
                    clipEventInitialize = bits.read_bool()
                    clipEventData = bits.read_bool()
                    bits.padding(5)
                    clipEventConstruct = bits.read_bool()
                    clipEventKeyPress = bits.read_bool()
                    clipEventDragOut = bits.read_bool()
                    bits.padding(8)
                return cls(
                    clipEventKeyUp,
                    clipEventKeyDown,
                    clipEventMouseUp,
                    clipEventMouseDown,
                    clipEventMouseMove,
                    clipEventUnload,
                    clipEventEnterFrame,
                    clipEventLoad,
                    clipEventDragOver,
                    clipEventRollOut,
                    clipEventRollOver,
                    clipEventReleaseOutside,
                    clipEventRelease,
                    clipEventPress,
                    clipEventInitialize,
                    clipEventData,
                    clipEventConstruct,
                    clipEventKeyPress,
                    clipEventDragOut,
                )

        @dataclass
        class ClipActionRecord:
            eventFlags: Any
            keyCode: int | None
            actions: ExtendedBuffer

        clipEventFlags: ClipEventFlags
        clipActionRecords: list[ClipActionRecord]

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            clipEventFlags = cls.ClipEventFlags.from_buffer(buffer)
            clipActionRecords = []
            for _ in range(clipEventFlags.getEventCount()):
                eventFlags = cls.ClipEventFlags.from_buffer(buffer)
                actionRecordSize = buffer.read_ui32()
                keyCode = buffer.read_ui8() if eventFlags.clipEventKeyPress else None
                actions = buffer.subbuffer(
                    actionRecordSize - (1 if eventFlags.clipEventKeyPress else 0)
                )
                # TODO: Implement proper ActionRecord parsing
                clipActionRecords.append(
                    cls.ClipActionRecord(eventFlags, keyCode, actions)
                )
            assert buffer.read_ui32() == 0  # ClipActionEndFlag must be 0!
            return cls(clipEventFlags, clipActionRecords)

    placeFlagMove: bool
    ratio: int | None
    name: str | None
    clipDepth: int | None
    clipActions: ClipActions | None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        with ExtendedBitIO(buffer) as bits:
            hasClipActions = bits.read_bool()
            hasClipDepth = bits.read_bool()
            hasName = bits.read_bool()
            hasRatio = bits.read_bool()
            hasColorTransform = bits.read_bool()
            hasMatrix = bits.read_bool()
            hasCharacter = bits.read_bool()
            placeFlagMove = bits.read_bool()
            depth = buffer.read_ui16()
            characterID = buffer.read_ui16() if hasCharacter else None
            matrix = Matrix.from_buffer(buffer) if hasMatrix else None
            colorTransform = (
                CxFormWithAlpha.with_alpha.from_buffer(buffer)
                if hasColorTransform
                else None
            )
            ratio = buffer.read_ui16() if hasRatio else None
            name = buffer.read_string() if hasName else None
            clipDepth = buffer.read_ui16() if hasClipDepth else None
            clipActions = (
                cls.ClipActions.from_buffer(buffer) if hasClipActions else None
            )
        return cls(
            characterID=characterID,
            depth=depth,
            matrix=matrix,
            colorTransform=colorTransform,
            placeFlagMove=placeFlagMove,
            ratio=ratio,
            name=name,
            clipDepth=clipDepth,
            clipActions=clipActions,
        )


Tag.register(PlaceObject2)
