from unittest import TestCase

from pyfdec.extended_buffer import ExtendedBuffer


class TestExtendedBuffer(TestCase):
    def test_subbuffer(self):
        buffer: ExtendedBuffer = ExtendedBuffer(b"Hello, World!")
        buffer.read(7)
        result: ExtendedBuffer = buffer.subbuffer(5)
        self.assertEqual(result.read(), b"World")


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
        data = b'\xC0\x01'
        buffer = ExtendedBuffer(data)
        self.assertEqual(buffer.read_fixed8(), 1.75)

    def test_fixed(self):
        # 00000000 00000001 11000000 00000000
        # 1.75
        # 0x00 0xC0 0x01 0x00
        data = b'\x00\xC0\x01\x00'
        buffer = ExtendedBuffer(data)
        self.assertEqual(buffer.read_fixed(), 1.75)

    def test_float16(self):
        # 1 01111 1000000000
        # -1.5
        # 0xBE 0x00
        data = b'\x00\xBE'
        buffer = ExtendedBuffer(data)
        self.assertEqual(buffer.read_f16(), -1.5)

    def test_float(self):
        # 1 01111111 10000000000000000000000
        # -1.5
        # 0XBF 0xC0 0x00 0x00
        data = b'\x00\x00\xC0\xBF'
        buffer = ExtendedBuffer(data)
        self.assertEqual(buffer.read_f32(), -1.5)

    def test_double(self):
        # 1 01111111111 1000000000000000000000000000000000000000000000000000
        # -1.5
        # 0xBF 0xF8 0x00 0x00 0x00 0x00 0x00 0x00
        data = b'\x00\x00\x00\x00\x00\x00\xF8\xBF'
        buffer = ExtendedBuffer(data)
        self.assertEqual(buffer.read_f64(), -1.5)

class TestEncodedU32(TestCase):
    def test_encodedu32_max(self):
        #
        data = b'\x7F'
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 127)
    
        
        # 1 111 1111 0 111 1111
        #   FF         7F
        # 00111111 11111111
        #     0x3F     0xFF
        data = b'\xFF\x7F'
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 16383)
        
        # 1 111 1111 1 111 1111 0 111 1111
        #   FF         FF         7F
        # 00011111 11111111 11111111
        #     0x3F     0xFF     0xFF
        data = b'\xFF\xFF\x7F'
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 2097151)
        
        # 1 111 1111 1 111 1111 1 111 1111 0 111 1111
        #   FF         FF         FF         7F
        # 00001111 11111111 11111111 11111111
        #     0x1F     0xFF     0xFF     0xFF
        data = b'\xFF\xFF\xFF\x7F'
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 268435455)
        
        # 1 111 1111 1 111 1111 1 111 1111 1 111 1111 0 000 1111
        #    FF         FF         FF         FF         0F
        # 11111111 11111111 11111111 11111111
        #     0xFF     0xFF     0xFF     0xFF
        data = b'\xFF\xFF\xFF\xFF\x0F'
        buffer = ExtendedBuffer(data)
        value = buffer.read_encoded_u32()
        self.assertEqual(value, 4294967295)
    
    def test_encodedu32_overflow(self):
        # 1 111 1111 1 111 1111 1 111 1111 1 111 1111 0 111 1111
        #    FF         FF         FF         FF         7F
        # 00000111 11111111 11111111 11111111 11111111
        #     0x07     0xFF     0xFF     0xFF     0xFF
        data = b'\xFF\xFF\xFF\xFF\x7F'
        buffer = ExtendedBuffer(data)
        with self.assertRaises(ValueError):
            buffer.read_encoded_u32()
            
        # 1 111 1111 1 111 1111 1 111 1111 1 111 1111 0 001 1111
        #    FF         FF         FF         FF         1F
        # 00000001 11111111 11111111 11111111 11111111
        #     0x01     0xFF     0xFF     0xFF     0xFF
        data = b'\xFF\xFF\xFF\xFF\x1F'
        buffer = ExtendedBuffer(data)
        with self.assertRaises(ValueError):
            buffer.read_encoded_u32()
    