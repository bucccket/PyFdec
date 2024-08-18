from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionBitAnd(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionBitAnd

Action.register(ActionBitAnd)

@dataclass
class ActionBitLShift(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionBitLShift

Action.register(ActionBitLShift)

@dataclass
class ActionBitOr(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionBitOr

Action.register(ActionBitOr)

@dataclass
class ActionBitRShift(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionBitRShift

Action.register(ActionBitRShift)

@dataclass
class ActionBitURShift(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionBitURShift

Action.register(ActionBitURShift)

@dataclass
class ActionBitXor(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionBitXor

Action.register(ActionBitXor)
