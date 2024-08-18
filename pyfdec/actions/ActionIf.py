from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionIf(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionIf

    branchOffset: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        branchOffset = buffer.read_si16()
        return cls(branchOffset)


Action.register(ActionIf)
