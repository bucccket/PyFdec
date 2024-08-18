from dataclasses import dataclass
from enum import Enum
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionNextFrame(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionNextFrame


Action.register(ActionNextFrame)


@dataclass
class ActionPrevFrame(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionPrevFrame


Action.register(ActionPrevFrame)


@dataclass
class ActionPlay(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionPlay


Action.register(ActionPlay)


@dataclass
class ActionStop(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionStop


Action.register(ActionStop)


@dataclass
class ActionToggleQualty(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionToggleQualty


Action.register(ActionToggleQualty)


@dataclass
class ActionStopSounds(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionStopSounds


Action.register(ActionStopSounds)


@dataclass
class ActionGoToLabel(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGoToLabel

    label: str

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        label = buffer.readString()
        return cls(label)


Action.register(ActionGoToLabel)


@dataclass
class ActionGetURL(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGetURL

    urlString: str
    targetString: str

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        urlString = buffer.readString()
        targetString = buffer.readString()
        return cls(urlString, targetString)


Action.register(ActionGetURL)


@dataclass
class ActionGotoFrame(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGotoFrame

    frame: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        frame = buffer.read_ui16()
        return cls(frame)


Action.register(ActionGotoFrame)


@dataclass
class ActionGotoFrame2(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGotoFrame2

    class PlayFlag(Enum):
        STOP = 0
        PLAY = 1

    playFlag: PlayFlag
    sceneBias: int | None = None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        hasSceneBias = buffer.read_bool()
        frame = buffer.read_ui16()
        if hasSceneBias:
            sceneBias = buffer.read_ui16()
            return cls(frame, sceneBias)
        return cls(frame)


Action.register(ActionGotoFrame2)


@dataclass
class ActionSetTarget(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionSetTarget

    targetName: str

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        targetName = buffer.readString()
        return cls(targetName)


Action.register(ActionSetTarget)


@dataclass
class ActionSetTarget2(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionSetTarget2


Action.register(ActionSetTarget2)


@dataclass
class ActionGetProperty(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionGetProperty


Action.register(ActionGetProperty)


@dataclass
class ActionSetProperty(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionSetProperty


Action.register(ActionSetProperty)
