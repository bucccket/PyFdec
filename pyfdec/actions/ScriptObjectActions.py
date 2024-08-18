from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionCallFunction(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionCallFunction


Action.register(ActionCallFunction)


@dataclass
class ActionCallMethod(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionCallMethod


Action.register(ActionCallMethod)


@dataclass
class ActionConstantPool(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionConstantPool

    constantPool: list[str]

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        count = buffer.read_ui16()
        constantPool = [buffer.read_string() for _ in range(count)]
        return cls(constantPool)


Action.register(ActionConstantPool)


@dataclass
class ActionDefineFunction(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionDefineFunction

    function_name: str
    params: list[str]
    code: ExtendedBuffer

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        function_name = buffer.read_string()
        param_count = buffer.read_ui16()
        params = [buffer.read_string() for _ in range(param_count)]
        code = buffer.subbuffer(buffer.read_ui16())
        return cls(function_name, params, code)


Action.register(ActionDefineFunction)


@dataclass
class ActionDefineLocal(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionDefineLocal


Action.register(ActionDefineLocal)


@dataclass
class ActionDefineLocal2(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionDefineLocal2


Action.register(ActionDefineLocal2)


@dataclass
class ActionDelete(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionDelete


Action.register(ActionDelete)


@dataclass
class ActionDelete2(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionDelete2


Action.register(ActionDelete2)


@dataclass
class ActionEnumerate(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionEnumerate


Action.register(ActionEnumerate)


@dataclass
class ActionEquals2(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionEquals2


Action.register(ActionEquals2)


@dataclass
class ActionGetMember(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGetMember


Action.register(ActionGetMember)


@dataclass
class ActionInitArray(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionInitArray


Action.register(ActionInitArray)


@dataclass
class ActionInitObject(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionInitObject


Action.register(ActionInitObject)


@dataclass
class ActionNewMethod(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionNewMethod


Action.register(ActionNewMethod)


@dataclass
class ActionNewObject(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionNewObject


Action.register(ActionNewObject)


@dataclass
class ActionSetMember(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionSetMember


Action.register(ActionSetMember)


@dataclass
class ActionTargetPath(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionTargetPath


Action.register(ActionTargetPath)


@dataclass
class ActionWith(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionWith

    size: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        size = buffer.read_ui16()
        return cls(size)


Action.register(ActionWith)
