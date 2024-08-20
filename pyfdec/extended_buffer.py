import io
import struct
from typing import Self


class ExtendedBuffer(io.BytesIO):
    def subbuffer(self, size: int) -> Self:
        return ExtendedBuffer(self.read(size))
    
    def bytes_left(self) -> int:
        return len(self.getbuffer()) - self.tell()

    def read_bool(self) -> bool:
        return self.read_ui8() == 1

    def read_si8(self) -> int:
        return int.from_bytes(self.read(1), byteorder="little", signed=True)

    def read_si16(self) -> int:
        return int.from_bytes(self.read(2), byteorder="little", signed=True)

    def read_si24(self) -> int:
        return int.from_bytes(self.read(3), byteorder="little", signed=True)

    def read_si32(self) -> int:
        return int.from_bytes(self.read(4), byteorder="little", signed=True)

    def read_ui8(self) -> int:
        return int.from_bytes(self.read(1), byteorder="little")

    def read_ui16(self) -> int:
        return int.from_bytes(self.read(2), byteorder="little")

    def read_ui24(self) -> int:
        return int.from_bytes(self.read(3), byteorder="little")

    def read_ui32(self) -> int:
        return int.from_bytes(self.read(4), byteorder="little")

    def read_ui64(self) -> int:
        return int.from_bytes(self.read(8), byteorder="little")

    def read_f16(self) -> float:
        return float(struct.unpack("e", self.read(2))[0])

    def read_f32(self) -> float:
        return float(struct.unpack("f", self.read(4))[0])

    def read_f64(self) -> float:
        return float(struct.unpack("d", self.read(8))[0])

    def read_fixed8(self) -> float:
        return float(self.read_ui16() / (1 << 8))

    def read_fixed(self) -> float:
        return float(self.read_ui32() / (1 << 16))

    def read_string(self) -> str:
        data = b""
        while (byte := self.read(1)) != b"\x00":
            data += byte
        return data.decode("utf-8")

    def read_encoded_u32(self) -> int:
        value = 0
        shift = 0
        while True:
            byte = self.read_ui8()
            value |= (byte & 0x7F) << shift
            if byte & 0x80 == 0:
                break
            shift += 7
        if value & 0x100000000:
            raise ValueError("EncodedU32 value is too large")
        return value

    def read_encoded_u30(self) -> int:
        return self.read_encoded_u32() & 0x3FFFFFFF

    def read_encoded_si32(self) -> int:
        return val - 0x100000000 if (val := self.read_encoded_u32()) & 0x80000000 else val
