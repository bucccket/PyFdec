from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionTrace(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionTrace

Action.register(ActionTrace)
