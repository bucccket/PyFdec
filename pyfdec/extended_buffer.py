import io
import struct
from typing import Self


class ExtendedBuffer(io.BytesIO):
    def subbuffer(self, size: int) -> Self:
        position = self.tell()
        return ExtendedBuffer(self.getvalue()[position:position+size])

    def read_si8(self) -> int:
        return int.from_bytes(self.read(1), byteorder='little', signed=True)
    
    def read_si16(self) -> int:
        return int.from_bytes(self.read(2), byteorder='little', signed=True)
    
    def read_si32(self) -> int:
        return int.from_bytes(self.read(4), byteorder='little', signed=True)
    
    def read_ui8(self) -> int:
        return int.from_bytes(self.read(1), byteorder='little')
    
    def read_ui16(self) -> int:
        return int.from_bytes(self.read(2), byteorder='little')
    
    def read_ui24(self) -> int:
        return int.from_bytes(self.read(3), byteorder='little')
    
    def read_ui32(self) -> int:
        return int.from_bytes(self.read(4), byteorder='little')
    
    def read_ui64(self) -> int:
        return int.from_bytes(self.read(8), byteorder='little')
    
    def read_f16(self) -> float:
        return float(struct.unpack('e', self.read(2))[0])
    
    def read_f32(self) -> float:
        return float(struct.unpack('f', self.read(4))[0])
    
    def read_f64(self) -> float:
        return float(struct.unpack('d', self.read(8))[0])
    
    def read_fixed8(self) -> float:
        return float(self.read_ui16() / (1<<8))
    
    def read_fixed(self) -> float:
        return float(self.read_ui32() / (1<<16))
    
    def read_string(self) -> str:
        data = b''
        while (byte := self.read(1)) != b'\x00':
            data += byte
        return data.decode('utf-8')
    