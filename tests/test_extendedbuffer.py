from unittest import TestCase

from pyfdec.extended_buffer import ExtendedBuffer


class TestExtendedBuffer(TestCase):
    def test_subbuffer(self):
        buffer: ExtendedBuffer = ExtendedBuffer(b"Hello, World!")
        buffer.read(7)
        result: ExtendedBuffer = buffer.subbuffer(5)
        self.assertEqual(result.read(), b"World")
