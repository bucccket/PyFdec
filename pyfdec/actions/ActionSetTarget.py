from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionSetTarget(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionSetTarget

    targetName: str

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        targetName = buffer.readString()
        return cls(targetName)


Action.register(ActionSetTarget)
