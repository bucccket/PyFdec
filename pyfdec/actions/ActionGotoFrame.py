from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionGotoFrame(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGotoFrame

    frame: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        frame = buffer.readUI16()
        return cls(frame)


Action.register(ActionGotoFrame)
