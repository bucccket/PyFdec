from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionAdd(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionAdd

Action.register(ActionAdd)

@dataclass
class ActionSubtract(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionSubtract

Action.register(ActionSubtract)

@dataclass
class ActionMultiply(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionMultiply

Action.register(ActionMultiply)

@dataclass
class ActionDivide(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionDivide

Action.register(ActionDivide)
