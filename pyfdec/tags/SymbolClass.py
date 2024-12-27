from dataclasses import dataclass
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.tags.Tag import Tag


@dataclass
class SymbolClass(Tag):
    tag_type: ClassVar[Tag.TagTypes] = Tag.TagTypes.SymbolClass

    symbols: list[tuple[int, str]]  # [tag id, class name]

    @property
    def num_symbols(self) -> int:
        return len(self.symbols)

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'SymbolClass':
        num_symbols = buffer.read_ui16()
        symbols = [(buffer.read_ui16(), buffer.read_string()) for _ in range(num_symbols)]
        return cls(symbols=symbols)


Tag.register(SymbolClass)
