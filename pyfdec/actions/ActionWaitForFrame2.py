from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionWaitForFrame2(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionWaitForFrame2

    skipCount: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        skipCount = buffer.read_ui8()
        return cls(skipCount)


Action.register(ActionWaitForFrame2)
