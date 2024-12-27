from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.StartSound import StartSound
from pyfdec.tags.Tag import Tag


@dataclass
class StartSound2(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.StartSound2

    soundClassName: str
    soundInfo: StartSound.SoundInfo

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'StartSound2':
        soundClassName = buffer.read_string()
        soundInfo = StartSound.SoundInfo.from_buffer(buffer)
        return cls(soundClassName=soundClassName, soundInfo=soundInfo)


Tag.register(StartSound2)
