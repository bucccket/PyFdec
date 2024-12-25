from pyfdec.bitio import BitIO


class ExtendedBitIO(BitIO):

    def read_unsigned(self, length: int) -> int:
        if length == 0:
            return 0
        data = self.read(length)
        val = 0
        for bit in data:
            val = (val << 1) | bit
        return val

    def read_signed(self, length: int) -> int:
        if length == 0:
            return 0
        data = self.read(length)
        val = 0
        for bit in data[1:]:
            val = (val << 1) | bit
        return val if data[0] == 0 else val - (1 << (length - 1))

    def read_fixed(self, length: int) -> float:
        if length == 0:
            return 0
        return self.read_unsigned(length) / (1 << 16)

    def read_bool(self) -> bool:
        return self.read(1)[0] == 1

    def padding(self, length: int) -> None:
        if length == 0:
            return 0
        self.read(length)

    def align(self) -> None:
        while len(self._buffer) % 8 != 0:
            self.read(1)
