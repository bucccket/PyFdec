from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionToInteger(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionToInteger


Action.register(ActionToInteger)


@dataclass
class ActionCharToAscii(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionCharToAscii


Action.register(ActionCharToAscii)


@dataclass
class ActionAsciiToChar(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionAsciiToChar


Action.register(ActionAsciiToChar)


@dataclass
class ActionMBAsciiToChar(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionMBAsciiToChar


Action.register(ActionMBAsciiToChar)


@dataclass
class ActionMBCharToAscii(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionMBCharToAscii


Action.register(ActionMBCharToAscii)


@dataclass
class ActionToNumber(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionToNumber


Action.register(ActionToNumber)


@dataclass
class ActionToString(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionToString


Action.register(ActionToString)


@dataclass
class ActionTypeOf(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionTypeOf


Action.register(ActionTypeOf)
