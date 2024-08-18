from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionNot(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionNot

    result: bool

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        result = buffer.read_bool()
        return cls(result)


Action.register(ActionNot)
