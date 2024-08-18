from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionStopSounds(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionStopSounds

Action.register(ActionStopSounds)
