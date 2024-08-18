from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionNextFrame(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionNextFrame

Action.register(ActionNextFrame)
