from unittest import TestCase

from bitarray import bitarray

from pyfdec.extended_bitio import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer

class TestExtendedBitIO(TestCase):
    def test_bit_io(self):
        data = b'\x01\x02\x03\x04\x05'
        buffer = ExtendedBuffer(data)
        bits = ExtendedBitIO(buffer)
        self.assertEqual(bits.read(1), bitarray('0'))
        self.assertEqual(bits.read(7), bitarray('0000001'))
        self.assertEqual(bits.read(16), bitarray('00000010 00000011'))
        self.assertEqual(buffer.read_ui8(), 4)
        
    def test_read_signed(self):
        # 11111 000
        # -1    0
        data = b'\xF8'
        buffer = ExtendedBuffer(data)
        bits = ExtendedBitIO(buffer)
        self.assertEqual(bits.read_signed(5), -1)
        self.assertEqual(bits.read_signed(3), 0)
    
    def test_read_float(self):
        # 00000000 00000000 . 00000000 00000000
        # 00000000 00000100 . 11000000 00000000
        # 4.75
        # 0x00 0x04 0xC0 0x00
        data = b'\x00\x04\xC0\x00'
        buffer = ExtendedBuffer(data)
        bits = ExtendedBitIO(buffer)
        self.assertEqual(bits.read_float(32), 4.75)