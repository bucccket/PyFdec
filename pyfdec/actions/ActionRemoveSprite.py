from dataclasses import dataclass
from typing import ClassVar
from pyfdec.actions.Action import Action
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ActionRemoveSprite(Action):
    action_code: ClassVar[Action.ActionCodes] = Action.ActionCodes.ActionRemoveSprite

Action.register(ActionRemoveSprite)
