from dataclasses import dataclass
from typing import ClassVar

from pyfdec.actions.Action import Action


@dataclass
class ActionGetVariable(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGetVariable


# Action.register(ActionGetVariable)


@dataclass
class ActionSetVariable(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionSetVariable


# Action.register(ActionSetVariable)
