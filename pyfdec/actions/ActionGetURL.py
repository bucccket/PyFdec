from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionGetURL(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGetURL

    urlString: str
    targetString: str

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        urlString = buffer.readString()
        targetString = buffer.readString()
        return cls(urlString, targetString)


Action.register(ActionGetURL)
