from collections import namedtuple
from dataclasses import dataclass
from pyfdec.abc.Traits import TraitInfo
from pyfdec.abc.Multinames import BaseMultiname, QName, RTQName, RTQNameL, Multiname, MultinameL, TypeName
from pyfdec.abc.Instructions import Instruction
from pyfdec.abc.ConstantKind import ConstantKind
from pyfdec.extended_buffer import ExtendedBuffer
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
            ints = [0]
            [ints.append(buffer.read_encoded_si32()) for _ in range(int_count - 1)]
            uint_count = buffer.read_encoded_u30()
            uints = [0]
            [uints.append(buffer.read_encoded_u32()) for _ in range(uint_count - 1)]
            double_count  = buffer.read_encoded_u30()
            doubles = [0]
            [doubles.append(buffer.read_f64()) for _ in range(double_count - 1)]
            string_count = buffer.read_encoded_u30()
            strings = [None]
            [strings.append(cls.read_abc_string(buffer)) for _ in range(string_count - 1)]
            namespace_count = buffer.read_encoded_u30()
            namespaces = [None]
            [namespaces.append(cls.NamespaceInfo.from_buffer(buffer)) for _ in range(namespace_count - 1)]
            namespace_set_count = buffer.read_encoded_u30()
            namespace_sets = [None]
            for _ in range(namespace_set_count - 1):
                count = buffer.read_ui8()
                namespace_sets.append([buffer.read_encoded_u30() for _ in range(count)]) 
            
            multiname_count = buffer.read_encoded_u30()
            multinames = [None]
            [multinames.append(cls.read_multiname(buffer)) for _ in range(multiname_count - 1)]

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
                value: int
                kind: ConstantKind

                @classmethod
                def from_buffer(cls, buffer: ExtendedBuffer):
                    value = buffer.read_encoded_u30()
                    kind = ConstantKind(buffer.read_ui8())
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

    @dataclass
    class InstanceInfo:
        class InstanceFlags(IntFlag):
            Sealed = 0x01
            Final = 0x02
            Interface = 0x04
            ProtectedNs = 0x08

        name: int
        super_name: int
        flags: InstanceFlags
        protected_ns: int | None
        interfaces: list[int]
        init: int
        traits: list[TraitInfo]

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            name = buffer.read_encoded_u30()
            super_name = buffer.read_encoded_u30()
            flags = cls.InstanceFlags(buffer.read_ui8())
            protected_ns = None
            if flags & cls.InstanceFlags.ProtectedNs:
                protected_ns = buffer.read_ui8()

            interface_count = buffer.read_encoded_u30()
            interfaces = [buffer.read_encoded_u30() for _ in range(interface_count)]
            init = buffer.read_encoded_u30()
            trait_count = buffer.read_encoded_u30()
            traits = [TraitInfo.from_buffer(buffer) for _ in range(trait_count)]

            return cls(
                name,
                super_name,
                flags,
                protected_ns,
                interfaces,
                init,
                traits
            )

    @dataclass
    class ClassInfo:
        init: int
        traits: list[TraitInfo]

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            init = buffer.read_encoded_u30()
            trait_count = buffer.read_encoded_u30()
            traits = [TraitInfo.from_buffer(buffer) for _ in range(trait_count)]

            return cls(init, traits)

    @dataclass
    class ScriptInfo:
        init: int
        traits: list[TraitInfo]

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            init = buffer.read_encoded_u30()
            trait_count = buffer.read_encoded_u30()
            traits = [TraitInfo.from_buffer(buffer) for _ in range(trait_count)]
            return cls(init, traits)

    @dataclass
    class MethodBodyInfo:
        @dataclass
        class ExceptionInfo:
            from_pos: int
            to_pos: int
            target: int
            exception_type: int
            var_name: int

            @classmethod
            def from_buffer(cls, buffer: ExtendedBuffer):
                from_pos = buffer.read_encoded_u30()
                to_pos = buffer.read_encoded_u30()
                target = buffer.read_encoded_u30()
                exception_type = buffer.read_encoded_u30()
                var_name = buffer.read_encoded_u30()
                return cls(
                    from_pos,
                    to_pos,
                    target,
                    exception_type,
                    var_name
                )

        method: int
        max_stack: int
        local_count: int
        init_scope_depth: int
        max_scope_depth: int

        code: list[Instruction]
        exceptions: list[ExceptionInfo]
        traits: list[TraitInfo]

        @classmethod
        def from_buffer(cls, buffer: ExtendedBuffer):
            method = buffer.read_encoded_u30()
            max_stack = buffer.read_encoded_u30()
            local_count = buffer.read_encoded_u30()
            init_scope_depth = buffer.read_encoded_u30()
            max_scope_depth = buffer.read_encoded_u30()

            code_length = buffer.read_encoded_u30()
            instruction_buffer = buffer.subbuffer(code_length)
            code = []
            while instruction_buffer.bytes_left():
                code.append(Instruction.from_buffer(instruction_buffer))
            
            exception_count = buffer.read_encoded_u30()
            exceptions = [cls.ExceptionInfo.from_buffer(buffer) for _ in range(exception_count)]
            trait_count = buffer.read_encoded_u30()
            traits = [TraitInfo.from_buffer(buffer) for _ in range(trait_count)]

            return cls(
                method,
                max_stack,
                local_count,
                init_scope_depth,
                max_scope_depth,
                code,
                exceptions,
                traits,
            )

    minor_version: int
    major_version: int
    cpool: CPoolInfo
    methods: list[MethodInfo]
    metadata: list[MetadataInfo]
    instances: list[InstanceInfo]
    classes: list[ClassInfo]
    scripts: list[ScriptInfo]
    method_bodies: list[MethodBodyInfo]
    
    @classmethod
    def from_buffer(cls, buffer: ExtendedBuffer):
        minor_version = buffer.read_ui16()
        major_version = buffer.read_ui16()
        cpool = cls.CPoolInfo.from_buffer(buffer)
        method_count = buffer.read_encoded_u30()
        methods = [cls.MethodInfo.from_buffer(buffer) for _ in range(method_count)]
        metadata_count = buffer.read_encoded_u30()
        metadata = [cls.MetadataInfo.from_buffer(buffer) for _ in range(metadata_count)]
        instance_count = buffer.read_encoded_u30()
        instances = [cls.InstanceInfo.from_buffer(buffer) for _ in range(instance_count)]
        classes = [cls.ClassInfo.from_buffer(buffer) for _ in range(instance_count)]
        script_count = buffer.read_encoded_u30()
        scripts = [cls.ScriptInfo.from_buffer(buffer) for _ in range(script_count)]
        method_body_count = buffer.read_encoded_u30()
        method_bodies = [cls.MethodBodyInfo.from_buffer(buffer) for _ in range(method_body_count)]

        return cls(
            minor_version,
            major_version,
            cpool,
            methods,
            metadata,
            instances,
            classes,
            scripts,
            method_bodies
        )
