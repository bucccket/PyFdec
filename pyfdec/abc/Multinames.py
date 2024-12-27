from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from pyfdec.extended_buffer import ExtendedBuffer


class BaseMultiname(ABC):

    class MultinameKind(Enum):
        QName = 0x07
        QNameA = 0x0D
        RTQName = 0x0F
        RTQNameA = 0x10
        RTQNameL = 0x11
        RTQNameLA = 0x12
        Multiname = 0x09
        MultinameA = 0x0E
        MultinameL = 0x1B
        MultinameLA = 0x1C
        TypeName = 0x1D

    multiname_kind: ClassVar[MultinameKind]

    @classmethod
    @abstractmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'BaseMultiname':
        pass


@dataclass
class QName(BaseMultiname):
    multiname_kind: ClassVar[BaseMultiname.MultinameKind] = BaseMultiname.MultinameKind.QName

    namespace: int
    name: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'QName':
        return cls(namespace=buffer.read_encoded_u30(), name=buffer.read_encoded_u30())


BaseMultiname.register(QName)


@dataclass
class RTQName(BaseMultiname):
    multiname_kind: ClassVar[BaseMultiname.MultinameKind] = BaseMultiname.MultinameKind.RTQName

    name: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'RTQName':
        return cls(name=buffer.read_encoded_u30())


BaseMultiname.register(RTQName)


@dataclass
class RTQNameL(BaseMultiname):
    multiname_kind: ClassVar[BaseMultiname.MultinameKind] = BaseMultiname.MultinameKind.RTQNameL

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'RTQNameL':
        return cls()


BaseMultiname.register(RTQNameL)


@dataclass
class Multiname(BaseMultiname):
    multiname_kind: ClassVar[BaseMultiname.MultinameKind] = BaseMultiname.MultinameKind.Multiname

    name: int
    namespace_set: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'Multiname':
        return cls(name=buffer.read_encoded_u30(), namespace_set=buffer.read_encoded_u30())


BaseMultiname.register(Multiname)


@dataclass
class MultinameL(BaseMultiname):
    multiname_kind: ClassVar[BaseMultiname.MultinameKind] = BaseMultiname.MultinameKind.MultinameL

    namespace_set: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'MultinameL':
        return cls(namespace_set=buffer.read_encoded_u30())


BaseMultiname.register(MultinameL)


@dataclass
class TypeName(BaseMultiname):
    multiname_kind: ClassVar[BaseMultiname.MultinameKind] = BaseMultiname.MultinameKind.TypeName

    name: int
    params: list[int]

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer) -> 'TypeName':
        name = buffer.read_encoded_u30()
        param_count = buffer.read_encoded_u30()
        params = [buffer.read_encoded_u30() for _ in range(param_count)]
        return cls(name, params)


BaseMultiname.register(TypeName)
