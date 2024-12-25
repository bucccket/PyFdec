from dataclasses import dataclass

from pyfdec.tags.DefineBits import DefineBits
from pyfdec.tags.Tag import Tag


@dataclass
class DefineBitsJPEG2(DefineBits):
    pass


Tag.register(DefineBitsJPEG2)
