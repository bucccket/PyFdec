from dataclasses import dataclass
from typing import ClassVar

from pyfdec.actions.Action import Action


@dataclass
class ActionEquals(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionEquals


# Action.register(ActionEquals)


@dataclass
class ActionStrictEquals(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionStrictEquals


# Action.register(ActionStrictEquals)


@dataclass
class ActionLess(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionLess


# Action.register(ActionLess)


@dataclass
class ActionLess2(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionLess2


# Action.register(ActionLess2)


@dataclass
class ActionGreater(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGreater


# Action.register(ActionGreater)
