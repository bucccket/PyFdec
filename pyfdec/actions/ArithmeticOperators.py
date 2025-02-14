from dataclasses import dataclass
from typing import ClassVar

from pyfdec.actions.Action import Action


@dataclass
class ActionAdd(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionAdd


# Action.register(ActionAdd)


@dataclass
class ActionAdd2(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionAdd2


# Action.register(ActionAdd2)


@dataclass
class ActionSubtract(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionSubtract


# Action.register(ActionSubtract)


@dataclass
class ActionMultiply(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionMultiply


# Action.register(ActionMultiply)


@dataclass
class ActionDivide(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionDivide


# Action.register(ActionDivide)


@dataclass
class ActionModulo(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionModulo


# Action.register(ActionModulo)


@dataclass
class ActionDecrement(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionDecrement


# Action.register(ActionDecrement)


@dataclass
class ActionIncrement(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionIncrement


# Action.register(ActionIncrement)
