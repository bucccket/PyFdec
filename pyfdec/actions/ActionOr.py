from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionOr(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionOr

Action.register(ActionOr)
