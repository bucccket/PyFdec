from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionStringEquals(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionStringEquals

Action.register(ActionStringEquals)

@dataclass
class ActionStringLength(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionStringLength

Action.register(ActionStringLength)


@dataclass
class ActionStringAdd(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionStringAdd

Action.register(ActionStringAdd)


@dataclass
class ActionStringExtract(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionStringExtract

Action.register(ActionStringExtract)

@dataclass
class ActionStringLess(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionStringLess

Action.register(ActionStringLess)

@dataclass
class ActionMBStringLength(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionMBStringLength

Action.register(ActionMBStringLength)

@dataclass
class ActionMBStringExtract(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionMBStringExtract

Action.register(ActionMBStringExtract)
