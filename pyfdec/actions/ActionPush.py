from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Union
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
