from unittest import TestCase

from pyfdec.extended_buffer import ExtendedBuffer


class TestReading(TestCase):
    def test_string(self):
        data = b"Hello, World!\x00"
        buffer = ExtendedBuffer(data)
        string = buffer.read_string()
        self.assertEqual(string, "Hello, World!")
