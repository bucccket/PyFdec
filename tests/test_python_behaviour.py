from unittest import TestCase

from bitarray import bitarray

from pyfdec.extended_bit_io import ExtendedBitIO
from pyfdec.extended_buffer import ExtendedBuffer


class DefineShape:
    def __init__(self):
        self.color = self.ReadColor()

    class ReadColor:
        def __init__(self):
            self.isUsingRGBA = False


class DefineShape2(DefineShape):

    class ReadColor:
        def __init__(self):
            self.isUsingRGBA = True


class TestExtendedBitIO(TestCase):
    def test_inheritance_rules(self):
        define_shape = DefineShape()
        self.assertFalse(define_shape.color.isUsingRGBA)

        define_shape_2 = DefineShape2()
        self.assertTrue(define_shape_2.color.isUsingRGBA)
