from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class StartSound(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.StartSound

    @dataclass
    class SoundInfo:

        @dataclass
        class SoundEnvelope:
            pos44: int
            leftLevel: int
            rightLevel: int

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer):
                pos44 = buffer.read_ui32()
                leftLevel = buffer.read_ui16()
                rightLevel = buffer.read_ui16()

                return cls(pos44=pos44, leftLevel=leftLevel, rightLevel=rightLevel)

        syncStop: bool
        syncNoMultiple: bool
        hasEnvelope: bool
        hasLoops: bool
        hasOutPoint: bool
        hasInPoint: bool
        inPoint: int | None
        outPoint: int | None
        loopCount: int | None
        envelopeRecords: list[SoundEnvelope]

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            with ExtendedBitIO(buffer) as bits:
                # Read reserved
                bits.read_unsigned(2)

                syncStop = bits.read_bool()
                syncNoMultiple = bits.read_bool()
                hasEnvelope = bits.read_bool()
                hasLoops = bits.read_bool()
                hasOutPoint = bits.read_bool()
                hasInPoint = bits.read_bool()

            inPoint = None
            if hasInPoint:
                inPoint = buffer.read_ui32()

            outPoint = None
            if hasOutPoint:
                outPoint = buffer.read_ui32()

            loopCount = None
            if hasLoops:
                loopCount = buffer.read_ui16()

            envelopeRecords = []
            if hasEnvelope:
                envPoints = buffer.read_ui8()
                for _ in range(envPoints):
                    envelopeRecords.append(cls.SoundEnvelope.from_buffer(buffer))

            return cls(
                syncStop=syncStop,
                syncNoMultiple=syncNoMultiple,
                hasEnvelope=hasEnvelope,
                hasLoops=hasLoops,
                hasOutPoint=hasOutPoint,
                hasInPoint=hasInPoint,
                inPoint=inPoint,
                outPoint=outPoint,
                loopCount=loopCount,
                envelopeRecords=envelopeRecords
            )

    soundId: int
    soundInfo: SoundInfo

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        soundId = buffer.read_ui16()
        soundInfo = cls.SoundInfo.from_buffer(buffer)
        return cls(soundId=soundId, soundInfo=soundInfo)


Tag.register(StartSound)
