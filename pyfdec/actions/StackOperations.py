from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionPush(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionPush

    class PushTypes(Enum):
        StringLiteral = 0
        FloatLiteral = 1
        Null = 2
        Undefined = 3
        Register = 4
        Boolean = 5
        Double = 6
        Integer = 7
        Constant8 = 8
        Constant16 = 9

    pushType: PushTypes
    value: str | float | int | bool | None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        pushType = cls.PushTypes(buffer.read_ui8())
        match pushType:
            case cls.PushTypes.StringLiteral:
                value = buffer.read_string()
            case cls.PushTypes.FloatLiteral:
                value = buffer.read_f32()
            case cls.PushTypes.Null:
                value = None
            case cls.PushTypes.Undefined:
                value = None
            case cls.PushTypes.Register:
                value = buffer.read_ui8()
            case cls.PushTypes.Boolean:
                value = buffer.read_bool()
            case cls.PushTypes.Double:
                value = buffer.read_f64()
            case cls.PushTypes.Integer:
                value = buffer.read_ui32()
            case cls.PushTypes.Constant8:
                value = buffer.read_ui8()
            case cls.PushTypes.Constant16:
                value = buffer.read_ui16()
        return cls(pushType, value)


Action.register(ActionPush)


@dataclass
class ActionPop(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionPop


Action.register(ActionPop)


@dataclass
class ActionPushDuplicate(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionPushDuplicate


Action.register(ActionPushDuplicate)


@dataclass
class ActionReturn(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionReturn


Action.register(ActionReturn)


@dataclass
class ActionStackSwap(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionStackSwap


Action.register(ActionStackSwap)


@dataclass
class ActionStoreRegister(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionStoreRegister

    register_number: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        register_number = buffer.read_ui8()
        return cls(register_number)


Action.register(ActionStoreRegister)
