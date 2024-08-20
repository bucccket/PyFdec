from collections import namedtuple
from dataclasses import dataclass
from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.avm2.Multinames import BaseMultiname, QName, RTQName, RTQNameL, Multiname, MultinameL, TypeName
from enum import Enum, IntFlag


@dataclass
class ABCFile:
    @dataclass
    class CPoolInfo:
        @dataclass
        class NamespaceInfo:
            class NamespaceKind(Enum):
                Namespace = 0x08
                PackageNamespace = 0x16
                PackageInternalNs = 0x17
                ProtectedNamespace = 0x18
                ExplicitNamespace = 0x19
                StaticProtectedNs = 0x1A
                PrivateNs = 0x05

            kind: NamespaceKind
            name: int

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer):
                kind = cls.NamespaceKind(buffer.read_ui8())
                name = buffer.read_encoded_u30()
                return cls(kind, name)


        ints: list[int]
        uints: list[int]
        doubles: list[float]
        strings: list[str]
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
                cls.NamespaceInfo.from_buffer(buffer)
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

    @dataclass
    class MethodInfo:
        class MethodFlags(IntFlag):
            NeedArguments = 0x01
            NeedActivation = 0x02
            NeedRest = 0x04
            HasOptional = 0x08
            SetDxns = 0x40
            HasParamNames = 0x80

        @dataclass
        class OptionInfo:
            @dataclass
            class OptionDetail:
                class ConstandKind(Enum):
                    Int = 0x03
                    UInt = 0x04
                    Double = 0x06
                    Utf8 = 0x01
                    Bool_True = 0x0B
                    Bool_False = 0x0A
                    Null = 0x0C
                    Undefined = 0x00
                    Namespace = 0x08
                    PackageNamespace = 0x16
                    PackageInternalNs = 0x17
                    ProtectedNamespace = 0x18
                    ExplicitNamespace = 0x19
                    StaticProtectedNs = 0x1A
                    PrivateNs = 0x05

                value: int
                kind: ConstandKind

                @classmethod
                def from_buffer(cls, buffer: ExtendedBuffer):
                    value = buffer.read_encoded_u30()
                    kind = cls.ConstandKind(buffer.read_ui8())
                    return cls(value, kind)


            details: list[OptionDetail]

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer):
                detail_count = buffer.read_encoded_u30()
                details = [cls.OptionDetail.from_buffer(buffer) for _ in range(detail_count)]
                return cls(details)


        return_type: int
        param_types: list[int]
        name: int
        flags: list[MethodFlags]
        option_info: list[OptionInfo] | None
        param_names: list[int] | None

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            param_count = buffer.read_encoded_u30()
            return_type = buffer.read_encoded_u30()
            param_types = [buffer.read_encoded_u30() for _ in range(param_count)]

            name = buffer.read_encoded_u30()
            flags = cls.MethodFlags(buffer.read_ui8())

            options = None
            if flags & cls.MethodFlags.HasOptional:
                options = cls.OptionInfo.from_buffer(buffer)
            
            param_names = None
            if flags & cls.MethodFlags.HasParamNames:
                param_names = [buffer.read_encoded_u30() for _ in range(param_count)]
            
            return cls(
                return_type,
                param_types,
                name,
                flags,
                options,
                param_names
            )

    @dataclass
    class MetadataInfo:

        @dataclass
        class ItemInfo:
            key: int            
            value: int

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer):
                return cls(key=buffer.read_encoded_u30(), value=buffer.read_encoded_u30())

        name: int
        items: list[ItemInfo]

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            name = buffer.read_encoded_u30()
            item_count = buffer.read_encoded_u30()
            items = [cls.ItemInfo.from_buffer(buffer) for _ in range(item_count)]
            return cls(name, items)


    minor_version: int
    major_version: int
    cpool: CPoolInfo
    methods: list[MethodInfo]
    metadata: list[MetadataInfo]
    
    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        minor_version = buffer.read_ui16()
        major_version = buffer.read_ui16()
        cpool = cls.CPoolInfo.from_buffer(buffer)
        method_count = buffer.read_encoded_u30()
        methods = [cls.MethodInfo.from_buffer(buffer) for _ in range(method_count)]
        metadata_count = buffer.read_encoded_u30()
        metadata = [cls.MetadataInfo.from_buffer(buffer) for _ in range(metadata_count)]

        return cls(
            minor_version,
            major_version,
            cpool,
            methods,
            metadata
        )
