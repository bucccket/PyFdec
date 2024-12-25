from dataclasses import dataclass
from typing import ClassVar

from pyfdec.actions.Action import Action
from pyfdec.extended_bit_io import ExtendedBitIO
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
class ActionEnumerate2(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionEnumerate2


Action.register(ActionEnumerate2)


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


@dataclass
class ActionDefineFunction2(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionDefineFunction2

    @dataclass
    class RegisterParam:
        register: int
        param_name: str

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            register = buffer.read_ui8()
            param_name = buffer.read_string()
            return cls(register, param_name)

    function_name: str
    register_count: int
    preload_parent: bool
    preload_root: bool
    suppress_super: bool
    preload_super: bool
    suppress_arguments: bool
    preload_arguments: bool
    suppress_this: bool
    preload_this: bool
    preload_global: bool
    params: list[RegisterParam]
    code: ExtendedBuffer

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        function_name = buffer.read_string()
        param_count = buffer.read_ui16()
        register_count = buffer.read_ui8()
        with ExtendedBitIO(buffer) as bits:
            preload_parent = bits.read_bool()
            preload_root = bits.read_bool()
            suppress_super = bits.read_bool()
            preload_super = bits.read_bool()
            suppress_arguments = bits.read_bool()
            preload_arguments = bits.read_bool()
            suppress_this = bits.read_bool()
            preload_this = bits.read_bool()
            bits.padding(7)
            preload_global = bits.read_bool()

        params = [cls.RegisterParam.from_buffer(buffer) for _ in range(param_count)]
        code = buffer.subbuffer(buffer.read_ui16())
        return cls(
            function_name,
            register_count,
            preload_parent,
            preload_root,
            suppress_super,
            preload_super,
            suppress_arguments,
            preload_arguments,
            suppress_this,
            preload_this,
            preload_global,
            params,
            code,
        )


Action.register(ActionDefineFunction2)


@dataclass
class ActionExtends(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionExtends


Action.register(ActionExtends)


@dataclass
class ActionCastOp(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionCastOp


Action.register(ActionCastOp)


@dataclass
class ActionImplementsOp(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionImplementsOp


Action.register(ActionImplementsOp)


@dataclass
class ActionTry(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionTry

    hasFinallyBlock: bool
    hasCatchBlock: bool
    catchNameOrRegister: str | int
    tryBody: ExtendedBuffer
    catchBody: ExtendedBuffer | None = None
    finallyBody: ExtendedBuffer | None = None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        with ExtendedBitIO(buffer) as bits:
            bits.padding(5)  #
            catchInRegister = bits.read_bool()
            hasFinallyBlock = bits.read_bool()
            hasCatchBlock = bits.read_bool()
            trySize = buffer.read_ui16()
            catchSize = buffer.read_ui16()
            finallySize = buffer.read_ui16()
            catchNameOrRegister = (
                buffer.read_string() if catchInRegister else buffer.read_ui8()
            )
            tryBody = buffer.subbuffer(trySize)
            catchBody = buffer.subbuffer(catchSize) if hasCatchBlock else None
            finallyBody = buffer.subbuffer(finallySize) if hasFinallyBlock else None
        return cls(
            hasFinallyBlock,
            hasCatchBlock,
            catchNameOrRegister,
            tryBody,
            catchBody,
            finallyBody,
        )


Action.register(ActionTry)


@dataclass
class ActionThrow(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionThrow


Action.register(ActionThrow)
