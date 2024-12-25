from unittest import TestCase


class DefineShape:

    class ReadColor:

        def __init__(self):
            self.isUsingRGBA: bool = False

    def __init__(self):
        self.color: self.ReadColor = self.ReadColor()


class DefineShape2(DefineShape):

    class ReadColor:

        def __init__(self):
            self.isUsingRGBA: bool = True


class TestExtendedBitIO(TestCase):

    def test_inheritance_rules(self):
        define_shape = DefineShape()
        self.assertFalse(define_shape.color.isUsingRGBA)

        define_shape_2 = DefineShape2()
        self.assertTrue(define_shape_2.color.isUsingRGBA)
