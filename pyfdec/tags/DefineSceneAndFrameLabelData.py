from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class DefineSceneAndFrameLabelData(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineSceneAndFrameLabelData

    @dataclass
    class SceneRecord:
        offset: int
        name: str

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer) -> 'DefineSceneAndFrameLabelData.SceneRecord':
            offset = buffer.read_ui32()
            name = buffer.read_string()
            return cls(offset, name)

    @dataclass
    class FrameLabelRecord:
        frameNum: int
        frameLabel: str

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer) -> 'DefineSceneAndFrameLabelData.FrameLabelRecord':
            frameNum = buffer.read_ui32()
            frameLabel = buffer.read_string()
            return cls(frameNum, frameLabel)

    scenes: list[SceneRecord]
    frameLabels: list[FrameLabelRecord]

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'DefineSceneAndFrameLabelData':
        sceneCount = buffer.read_encoded_u32()
        scenes = [cls.SceneRecord.from_buffer(buffer) for _ in range(sceneCount)]
        frameLabelCount = buffer.read_encoded_u32()
        frameLabels = [cls.FrameLabelRecord.from_buffer(buffer) for _ in range(frameLabelCount)]
        return cls(scenes, frameLabels)


Tag.register(DefineSceneAndFrameLabelData)
