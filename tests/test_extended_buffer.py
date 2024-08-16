from unittest import TestCase

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer


class TestExtendedBuffer(TestCase):
    def test_subbuffer(self):
        buffer: ExtendedBuffer = ExtendedBuffer(b"Hello, World!")
        buffer.read(7)
        result: ExtendedBuffer = buffer.subbuffer(5)
        self.assertEqual(result.read(), b"World")
        self.assertEqual(buffer.read(1), b"!")

    def test_bitbuffer_position(self):
        buffer: ExtendedBuffer = ExtendedBuffer(b"Hello, World!")
        with ExtendedBitIO(buffer) as bits:
            bits.read(8 * 7)  # "Hello, "
        string = buffer.read(5)
        self.assertEqual(buffer.tell(), 12)
        self.assertEqual(string, b"World")


class TestReading(TestCase):
    def test_string(self):
        data = b"Hello, World!\x00"
        buffer = ExtendedBuffer(data)
        string = buffer.read_string()
        self.assertEqual(string, "Hello, World!")

    def test_fixed8(self):
        # 00000001 11000000
        # 1.75
        # 0x01 0xC0
        data = b"\xC0\x01"
        buffer = ExtendedBuffer(data)
        self.assertEqual(buffer.read_fixed8(), 1.75)

    def test_fixed(self):
        # 00000000 00000001 11000000 00000000
        # 1.75
        # 0x00 0xC0 0x01 0x00
        data = b"\x00\xC0\x01\x00"
        buffer = ExtendedBuffer(data)
        self.assertEqual(buffer.read_fixed(), 1.75)

    def test_float16(self):
        # 1 01111 1000000000
        # -1.5
        # 0xBE 0x00
        data = b"\x00\xBE"
        buffer = ExtendedBuffer(data)
        self.assertEqual(buffer.read_f16(), -1.5)

    def test_float(self):
        # 1 01111111 10000000000000000000000
        # -1.5
        # 0XBF 0xC0 0x00 0x00
        data = b"\x00\x00\xC0\xBF"
        buffer = ExtendedBuffer(data)
        self.assertEqual(buffer.read_f32(), -1.5)

    def test_double(self):
        # 1 01111111111 1000000000000000000000000000000000000000000000000000
        # -1.5
        # 0xBF 0xF8 0x00 0x00 0x00 0x00 0x00 0x00
        data = b"\x00\x00\x00\x00\x00\x00\xF8\xBF"
        buffer = ExtendedBuffer(data)
        self.assertEqual(buffer.read_f64(), -1.5)


class TestEncodedU32(TestCase):
    def test_encodedu32_max(self):
        #
        data = b"\x7F"
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 127)

        # 1 111 1111 0 111 1111
        #   FF         7F
        # 00111111 11111111
        #     0x3F     0xFF
        data = b"\xFF\x7F"
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 16383)

        # 1 111 1111 1 111 1111 0 111 1111
        #   FF         FF         7F
        # 00011111 11111111 11111111
        #     0x3F     0xFF     0xFF
        data = b"\xFF\xFF\x7F"
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 2097151)

        # 1 111 1111 1 111 1111 1 111 1111 0 111 1111
        #   FF         FF         FF         7F
        # 00001111 11111111 11111111 11111111
        #     0x1F     0xFF     0xFF     0xFF
        data = b"\xFF\xFF\xFF\x7F"
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 268435455)

        # 1 111 1111 1 111 1111 1 111 1111 1 111 1111 0 000 1111
        #    FF         FF         FF         FF         0F
        # 11111111 11111111 11111111 11111111
        #     0xFF     0xFF     0xFF     0xFF
        data = b"\xFF\xFF\xFF\xFF\x0F"
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 4294967295)

    def test_encodedu32_overflow(self):
        # 1 111 1111 1 111 1111 1 111 1111 1 111 1111 0 111 1111
        #    FF         FF         FF         FF         7F
        # 00000111 11111111 11111111 11111111 11111111
        #     0x07     0xFF     0xFF     0xFF     0xFF
        data = b"\xFF\xFF\xFF\xFF\x7F"
        buffer = ExtendedBuffer(data)
        with self.assertRaises(ValueError):
            buffer.read_encoded_u32()

        # 1 111 1111 1 111 1111 1 111 1111 1 111 1111 0 001 1111
        #    FF         FF         FF         FF         1F
        # 00000001 11111111 11111111 11111111 11111111
        #     0x01     0xFF     0xFF     0xFF     0xFF
        data = b"\xFF\xFF\xFF\xFF\x1F"
        buffer = ExtendedBuffer(data)
        with self.assertRaises(ValueError):
            buffer.read_encoded_u32()

    def test_encodedu32_arbitrary_values(self):
        data = b"\x40"
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 64)

        # 1 101 1001 0 001 1001
        # D919
        # 00001100 11011001
        # 3289

        data = b"\xD9\x19"
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 3289)

        # 1 101 1001 1 101 1001 0 001 1001
        # D9 D919
        # 00000110 01101100 11011001
        # 421081

        data = b"\xD9\xD9\x19"
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 421081)

        # 1 100 0011 1 101 1001 1 101 1001 0 001 1001
        # C3D9 D919
        # 000011 00110110 01101100 11000011
        # 53898435

        data = b"\xC3\xD9\xD9\x19"
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 53898435)

        # 1 000 1111 1 100 0011 1 101 1001 1 101 1001 0 000 1001
        # 8FC3D9D909
        # 000 1001 101 1001 101 1001 100 0011 000 1111
        # 2604032399

        data = b"\x8F\xC3\xD9\xD9\x09"
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 2604032399)
