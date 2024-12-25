from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer


class Action(ABC):

    class ActionCodes(Enum):
        ActionGotoFrame = 0x81
        ActionGetURL = 0x83
        ActionNextFrame = 0x04
        ActionPreviousFrame = 0x05
        ActionPlay = 0x06
        ActionStop = 0x07
        ActionToggleQuality = 0x08
        ActionStopSounds = 0x09
        ActionWaitForFrame = 0x8A
        ActionSetTarget = 0x8B
        ActionGoToLabel = 0x8C
        ActionPush = 0x96
        ActionPop = 0x17
        ActionAdd = 0x0A
        ActionSubtract = 0x0B
        ActionMultiply = 0x0C
        ActionDivide = 0x0D
        ActionEquals = 0x0E
        ActionLess = 0x0F
        ActionAnd = 0x10
        ActionOr = 0x11
        ActionNot = 0x12
        ActionStringEquals = 0x13
        ActionStringLength = 0x14
        ActionStringAdd = 0x21
        ActionStringExtract = 0x15
        ActionStringLess = 0x29
        ActionMBStringLength = 0x31
        ActionMBStringExtract = 0x35
        ActionToInteger = 0x18
        ActionCharToAscii = 0x32
        ActionAsciiToChar = 0x33
        ActionMBCharToAscii = 0x36
        ActionMBAsciiToChar = 0x37
        ActionJump = 0x99
        ActionIf = 0x9D
        ActionCall = 0x9E
        ActionGetVariable = 0x1C
        ActionSetVariable = 0x1D
        ActionGetURL2 = 0x9A
        ActionGotoFrame2 = 0x9F
        ActionSetTarget2 = 0x20
        ActionGetProperty = 0x22
        ActionSetProperty = 0x23
        ActionCloneSprite = 0x24
        ActionRemoveSprite = 0x25
        ActionStartDrag = 0x27
        ActionEndDrag = 0x28
        ActionWaitForFrame2 = 0x8D
        ActionTrace = 0x26
        ActionGetTime = 0x34
        ActionRandomNumber = 0x30
        ActionCallFunction = 0x3D
        ActionCallMethod = 0x52
        ActionConstantPool = 0x88
        ActionDefineFunction = 0x9B
        ActionDefineLocal = 0x3C
        ActionDefineLocal2 = 0x41
        ActionDelete = 0x3A
        ActionDelete2 = 0x3B
        ActionEnumerate = 0x46
        ActionEquals2 = 0x49
        ActionGetMember = 0x4E
        ActionInitArray = 0x42
        ActionInitObject = 0x43
        ActionNewMethod = 0x53
        ActionNewObject = 0x40
        ActionSetMember = 0x4F
        ActionTargetPath = 0x45
        ActionWith = 0x94
        ActionToNumber = 0x4A
        ActionToString = 0x4B
        ActionTypeOf = 0x44
        ActionAdd2 = 0x47
        ActionLess2 = 0x48
        ActionModulo = 0x3F
        ActionBitAnd = 0x60
        ActionBitLShift = 0x63
        ActionBitOr = 0x61
        ActionBitRShift = 0x64
        ActionBitURShift = 0x65
        ActionBitXor = 0x62
        ActionDecrement = 0x51
        ActionIncrement = 0x50
        ActionPushDuplicate = 0x4C
        ActionReturn = 0x3E
        ActionStackSwap = 0x4D
        ActionStoreRegister = 0x87
        ActionInstanceOf = 0x54
        ActionEnumerate2 = 0x55
        ActionStrictEquals = 0x66
        ActionGreater = 0x67
        ActionStringGreater = 0x68
        ActionExtends = 0x69
        ActionCastOp = 0x2B
        ActionImplementsOp = 0x2C
        ActionTry = 0x8F
        ActionThrow = 0x2A

    action_code: ClassVar[ActionCodes]

    @classmethod
    @abstractmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        pass


@dataclass
class ActionRecord:
    action_code: Action.ActionCodes
    action_length: int | None = None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        action_code = Action.ActionCodes(buffer.read_ui8())
        if action_code.value >= 0x80:
            action_length = buffer.read_ui16()
            return cls(action_code, action_length)
        return cls(action_code)
