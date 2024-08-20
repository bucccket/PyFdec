from collections import namedtuple
from dataclasses import dataclass
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.avm2.Multinames import * 


@dataclass
class ABCFile:
    minor_version: int
    major_version: int

    @dataclass
    class CPoolInfo:
        ints: list[int]
        uints: list[int]
        doubles: list[float]
        strings: list[str]

        NamespaceInfo = namedtuple("NamespaceInfo", ["kind", "name"])
        namespaces: list[NamespaceInfo]

        namespace_sets: list[list[int]]
        multinames: list[BaseMultiname]

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            int_count = buffer.read_encoded_u30()
            ints = [buffer.read_encoded_si32() for _ in range(int_count - 1)]
            uint_count = buffer.read_encoded_u30()
            uints = [buffer.read_encoded_u32() for _ in range(uint_count - 1)]
            double_count  = buffer.read_encoded_u30()
            doubles = [buffer.read_f64() for _ in range(double_count - 1)]
            string_count = buffer.read_encoded_u30()
            strings = [cls.read_abc_string(buffer) for _ in range(string_count - 1)]
            namespace_count = buffer.read_encoded_u30()
            namespaces = [
                cls.NamespaceInfo(kind=buffer.read(1), name=buffer.read_encoded_u30()) 
                for _ in range(namespace_count - 1)
            ]
            namespace_set_count = buffer.read_encoded_u30()
            namespace_sets = []
            for _ in range(namespace_set_count - 1):
                count = buffer.read_ui8()
                namespace_sets.append([buffer.read_encoded_u30() for _ in range(count)]) 
            
            multiname_count = buffer.read_encoded_u30()
            multinames = [cls.read_multiname(buffer) for _ in range(multiname_count - 1)]

            return cls(
                ints,
                uints,
                doubles,
                strings,
                namespaces,
                namespace_sets,
                multinames
            )
        
        @staticmethod
        def read_abc_string(buffer: ExtendedBuffer) -> str:
            length = buffer.read_encoded_u30()
            data = buffer.read(length)
            return data.decode("utf-8")

        @staticmethod
        def read_multiname(buffer: ExtendedBuffer) -> BaseMultiname:
            kind = BaseMultiname.MultinameKind(buffer.read_ui8())
            match kind:
                case BaseMultiname.MultinameKind.QName | BaseMultiname.MultinameKind.QNameA:
                    return QName.from_buffer(buffer)
                case BaseMultiname.MultinameKind.RTQName | BaseMultiname.MultinameKind.RTQNameA:
                    return RTQName.from_buffer(buffer)
                case BaseMultiname.MultinameKind.RTQNameL | BaseMultiname.MultinameKind.RTQNameLA:
                    return RTQNameL.from_buffer(buffer)
                case BaseMultiname.MultinameKind.Multiname | BaseMultiname.MultinameKind.MultinameA:
                    return Multiname.from_buffer(buffer)
                case BaseMultiname.MultinameKind.MultinameL | BaseMultiname.MultinameKind.MultinameLA:
                    return MultinameL.from_buffer(buffer)
                case BaseMultiname.MultinameKind.TypeName:
                    return TypeName.from_buffer(buffer)
                case _:
                    raise NotImplementedError(f"Unimplemented multiname type: {kind}")


    cpool: CPoolInfo
    
    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        minor_version = buffer.read_ui16()
        major_version = buffer.read_ui16()
        cpool = cls.CPoolInfo.from_buffer(buffer)

        return cls(
            minor_version,
            major_version,
            cpool
        )
