from collections import namedtuple
from dataclasses import dataclass

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer


@dataclass
class ABCFile:
    minor_version: int
    major_version: int

    @dataclass
    class CPoolInfo:
        ints: list[int]
        uints: list[int]  # int... this feels wrong
        doubles: list[float]
        strings: list[str]

        NamespaceInfo = namedtuple("NamespaceInfo", ["kind", "name"])
        namespaces: list[NamespaceInfo]

        namespace_sets: list[list[int]]
        multinames: list[int] # TODO

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
            
            # TODO: multinames

            return cls(
                ints,
                uints,
                doubles,
                strings,
                namespaces,
                namespace_sets,
                multinames=[]
            )
        
        @staticmethod
        def read_abc_string(buffer: ExtendedBuffer) -> str:
            length = buffer.read_encoded_u30()
            data = buffer.read(length)
            return data.decode("utf-8")

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
