from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum, IntFlag
from typing import ClassVar
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.avm2.ConstantKind import ConstantKind


class TraitAttributes(IntFlag):
    Attrbute_None = 0x0
    Final = 0x1
    Override = 0x2
    Metadata = 0x4


class TraitType(Enum):
    Slot = 0
    Method = 1
    Getter = 2
    Setter = 3
    Class = 4
    Function = 5
    Const = 6


class BaseTrait(ABC):
    trait_type: ClassVar[TraitType]

    @classmethod
    @abstractmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        pass


@dataclass
class SlotTrait(BaseTrait):
    trait_type: ClassVar[TraitType] = TraitType.Slot

    id: int
    typename: int
    v_index: int
    v_kind: ConstantKind | None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        id = buffer.read_encoded_u30()
        typename = buffer.read_encoded_u30()
        v_index = buffer.read_encoded_u30()
        v_kind = buffer.read_ui8() if v_index > 0 else None
        return cls(
            id,
            typename,
            v_index,
            v_kind
        )


BaseTrait.register(SlotTrait)


@dataclass
class ClassTrait(BaseTrait):
    trait_type: ClassVar[TraitType] = TraitType.Class

    id: int
    class_index: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        id = buffer.read_encoded_u30()
        class_index = buffer.read_encoded_u30()
        return cls(id, class_index)


BaseTrait.register(ClassTrait)


@dataclass
class MethodTrait(BaseTrait):
    trait_type: ClassVar[TraitType] = TraitType.Method

    id: int
    method_index: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        id = buffer.read_encoded_u30()
        method_index = buffer.read_encoded_u30()
        return cls(id, method_index)


BaseTrait.register(MethodTrait)


@dataclass
class FunctionTrait(BaseTrait):
    trait_type: ClassVar[TraitType] = TraitType.Function

    id: int
    function_index: int

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        id = buffer.read_encoded_u30()
        function_index = buffer.read_encoded_u30()
        return cls(id, function_index)


BaseTrait.register(FunctionTrait)


@dataclass
class TraitInfo:
    
    name: int
    attributes: TraitAttributes
    kind: TraitType
    trait: BaseTrait
    metadata: list[int] | None

    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        name = buffer.read_encoded_u30()
        kind_attributes = buffer.read_ui8()
        kind = TraitType(kind_attributes & 0x0F)
        attributes = TraitAttributes(kind_attributes >> 4)

        match kind:
            case TraitType.Slot | TraitType.Const:
                trait = SlotTrait.from_buffer(buffer)
            case TraitType.Class:
                trait = ClassTrait.from_buffer(buffer)
            case TraitType.Function:
                trait = FunctionTrait.from_buffer(buffer)
            case TraitType.Method | TraitType.Getter | TraitType.Setter:
                trait = MethodTrait.from_buffer(buffer)
            case _:
                raise NotImplementedError(f"Unimplemented trait type: {kind}")
            
        metadata = None
        if attributes & TraitAttributes.Metadata:
            metadata_count = buffer.read_encoded_u30()
            metadata = [buffer.read_encoded_u30() for _ in range(metadata_count)]

        return cls(
            name,
            attributes,
            kind,
            trait,
            metadata
        )
