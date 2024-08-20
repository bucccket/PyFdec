from dataclasses import dataclass
from typing import ClassVar
from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import RGB
from pyfdec.tags.End import End
from pyfdec.tags.FrameLabel import FrameLabel
from pyfdec.tags.PlaceObject import PlaceObject
from pyfdec.tags.PlaceObject2 import PlaceObject2
from pyfdec.tags.PlaceObject3 import PlaceObject3
from pyfdec.tags.RemoveObject import RemoveObject
from pyfdec.tags.RemoveObject2 import RemoveObject2
from pyfdec.tags.SetBackgroundColor import SetBackgroundColor
from pyfdec.tags.ShowFrame import ShowFrame
from pyfdec.tags.StartSound import StartSound
from pyfdec.tags.Tag import Tag, TagHeader


@dataclass
class DefineSprite(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.DefineSprite

    spriteID: int
    frameCount: int
    tags: list[Tag]

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        spriteID = buffer.read_ui16()
        frameCount = buffer.read_ui16()
        tags = []
        while True:
            tag_header = TagHeader.from_buffer(buffer)

            tag_buffer = buffer.subbuffer(tag_header.tag_length)
            match tag_header.tag_type:
                # Supported Control Tags
                case Tag.TagTypes.ShowFrame:
                    tags.append(ShowFrame.from_buffer(tag_buffer))
                case Tag.TagTypes.PlaceObject:
                    tags.append(PlaceObject.from_buffer(tag_buffer))
                case Tag.TagTypes.PlaceObject2:
                    tags.append(PlaceObject2.from_buffer(tag_buffer))
                case Tag.TagTypes.PlaceObject3:
                    tags.append(PlaceObject3.from_buffer(tag_buffer))
                case Tag.TagTypes.RemoveObject:
                    tags.append(RemoveObject.from_buffer(tag_buffer))
                case Tag.TagTypes.RemoveObject2:
                    tags.append(RemoveObject2.from_buffer(tag_buffer))
                case Tag.TagTypes.StartSound:
                    tags.append(StartSound.from_buffer(tag_buffer))
                case Tag.TagTypes.FrameLabel:
                    tags.append(FrameLabel.from_buffer(tag_buffer))
                case Tag.TagTypes.SoundStreamHead:
                    raise NotImplementedError("DefineSprite SoundStreamHead")
                case Tag.TagTypes.SoundStreamHead2:
                    raise NotImplementedError("DefineSprite SoundStreamHead2")
                case Tag.TagTypes.SoundStreamBlock:
                    raise NotImplementedError("DefineSprite SoundStreamBlock")
                # Action Tags
                case Tag.TagTypes.DoAction:
                    raise NotImplementedError("DefineSprite DoAction")
                case Tag.TagTypes.DoInitAction:
                    raise NotImplementedError("DefineSprite DoInitAction")
                case Tag.TagTypes.DoABC:
                    raise NotImplementedError("DefineSprite DoABC")
                case Tag.TagTypes.End:
                    tags.append(End.from_buffer(tag_buffer))
                    break
                case _:
                    raise ValueError(
                        f"DefineSprite Unsupported Tag: {tag_header.tag_type}"
                    )
        return cls(spriteID, frameCount, tags)


Tag.register(DefineSprite)
