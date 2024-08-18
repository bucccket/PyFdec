from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionGoToLabel(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGoToLabel

    label: str

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        label = buffer.readString()
        return cls(label)


Action.register(ActionGoToLabel)
