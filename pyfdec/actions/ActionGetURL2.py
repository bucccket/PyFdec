from dataclasses import dataclass
from enum import Enum
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionGetURL2(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGetURL2

    class SendVarsMethod(Enum):
        NONE = 0
        GET = 1
        POST = 2

    class LoadTargetFlag(Enum):
        IsBrowserWindow = 0
        IsPathToSprite = 1

    class LoadVariablesFlag(Enum):
        NotLoad = 0
        Load = 1

    sendVarsMethod: SendVarsMethod
    loadTargetFlag: LoadTargetFlag
    loadVariablesFlag: LoadVariablesFlag

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        with ExtendedBitIO(buffer) as bits:
            sendVarsMethod = cls.SendVarsMethod(bits.read_unsigned_bits(2))
            bits.padding(4)
            loadTargetFlag = cls.LoadTargetFlag(bits.read_unsigned_bits(1))
            loadVariablesFlag = cls.LoadVariablesFlag(bits.read_unsigned_bits(1))

        return cls(sendVarsMethod, loadTargetFlag, loadVariablesFlag)


Action.register(ActionGetURL2)
