from dataclasses import dataclass
from enum import Enum
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionGotoFrame(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGotoFrame

    class PlayFlag(Enum):
        STOP = 0
        PLAY = 1
    
    playFlag: PlayFlag
    sceneBias: int | None = None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        hasSceneBias = buffer.read_bool()
        frame = buffer.read_ui16()
        if hasSceneBias:
            sceneBias = buffer.read_ui16()
            return cls(frame, sceneBias)
        return cls(frame)


Action.register(ActionGotoFrame)
