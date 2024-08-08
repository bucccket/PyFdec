from unittest import TestCase

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.color_types import ARGB, RGB, RGBA, CxForm, CxFormAlpha
from pyfdec.record_types.geometric_types import Matrix, Rect


class TestReading(TestCase):
    def test_rect(self):
        # layout
        # nbits xmin xmax ymin ymax
        # 00100 0000 0100 0010 0110
        #     4    0    4    2    6
        # 00100000 00100001 00110000
        #     0x20     0x21     0x30
        data = b'\x20\x21\x30'
        buffer = ExtendedBuffer(data)
        rect = Rect.from_buffer(buffer)
        self.assertEqual(rect.xmin, 0)
        self.assertEqual(rect.xmax, 4)
        self.assertEqual(rect.ymin, 2)
        self.assertEqual(rect.ymax, 6)
        
        # nbits xmin xmax ymin ymax
        # 00100 1111 0100 1110 0110
        #     4   -1    4   -2    6
        # 00100111 10100111 00110000
        #     0x27     0xA7     0x30

        data = b'\x27\xA7\x30'
        buffer = ExtendedBuffer(data)
        rect = Rect.from_buffer(buffer)
        self.assertEqual(rect.xmin, -1)
        self.assertEqual(rect.xmax, 4)
        self.assertEqual(rect.ymin, -2)
        self.assertEqual(rect.ymax, 6)
    
    def test_matrix(self):
        # simple matrix
        # hasScale = 0, hasRotate = 0
        # SR nbits x    y
        # 00 00100 0100 0010
        # FF 4     4    2
        # 00001000 10000100
        #     0x08     0x84
        data = b'\x08\x84'
        buffer = ExtendedBuffer(data)
        matrix = Matrix.from_buffer(buffer)
        self.assertEqual(matrix.translate_x, 4)
        self.assertEqual(matrix.translate_y, 2)
        
        # scale only matrix
        # hasScale = 1, hasRotate = 0
        # S nbits scaleX            scaleY            R nbits x    y
        # 1 10001 11000000000000000 10100000000000000 0 00100 0100 0010
        # T 17    1.5               1.25              F 4     4    2
        # 11000111 00000000 00000001 01000000 00000000 00010001 00001000
        #     0xC7     0x00     0x01     0x40     0x00     0x11     0x08
        data = b'\xC7\x00\x01\x40\x00\x11\x08'
        buffer = ExtendedBuffer(data)
        matrix = Matrix.from_buffer(buffer)
        self.assertEqual(matrix.translate_x, 4)
        self.assertEqual(matrix.translate_y, 2)
        self.assertEqual(matrix.scale_x, 1.5)
        self.assertEqual(matrix.scale_y, 1.25)

        # rotate only matrix
        # hasScale = 0, hasRotate = 1
        # SR nbits rotateSkew0       rotateSkew1       nbits x    y
        # 01 10001 11000000000000000 10100000000000000 00100 0100 0010
        # FT 17    1.5               1.25              4     4    2
        # 01100011 10000000 00000000 10100000 00000000 00010001 00001000
        #     0x63     0x80     0x00     0xA0     0x00     0x11     0x08
        data = b'\x63\x80\x00\xA0\x00\x11\x08'
        buffer = ExtendedBuffer(data)
        matrix = Matrix.from_buffer(buffer)
        self.assertEqual(matrix.translate_x, 4)
        self.assertEqual(matrix.translate_y, 2)
        self.assertEqual(matrix.rotate_skew0, 1.5)
        self.assertEqual(matrix.rotate_skew1, 1.25)
        
        # scale and rotate matrix
        # hasScale = 1, hasRotate = 1
        # S nbits scaleX            scaleY            R nbits rotateSkew0       rotateSkew1       nbits x    y
        # 1 10001 11000000000000000 10100000000000000 1 10001 10010000000000000 10001000000000000 00100 0100 0010
        # T 17    1.5               1.25              T 17    1.125             1.0625            4     4    2
        # 11000111 00000000 00000001 01000000 00000000 11000110 01000000 00000001 00010000 00000000 00100010 00010000
        #     0xC7     0x00     0x01     0x40     0x00     0xC6     0x40     0x01     0x10     0x00     0x22     0x10
        data = b'\xC7\x00\x01\x40\x00\xC6\x40\x01\x10\x00\x22\x10'
        buffer = ExtendedBuffer(data)
        matrix = Matrix.from_buffer(buffer)
        self.assertEqual(matrix.translate_x, 4)
        self.assertEqual(matrix.translate_y, 2)
        self.assertEqual(matrix.scale_x, 1.5)
        self.assertEqual(matrix.scale_y, 1.25)
        self.assertEqual(matrix.rotate_skew0, 1.125)
        self.assertEqual(matrix.rotate_skew1, 1.0625)

    def test_rgb(self):
        data = b'\x00\xFF\x00'
        buffer = ExtendedBuffer(data)
        rgb = RGB.from_buffer(buffer)
        self.assertEqual(rgb.red, 0)
        self.assertEqual(rgb.green, 255)
        self.assertEqual(rgb.blue, 0)
    
    def test_rgba(self):
        data = b'\x00\xFF\x00\xFF'
        buffer = ExtendedBuffer(data)
        rgba = RGBA.from_buffer(buffer)
        self.assertEqual(rgba.red, 0)
        self.assertEqual(rgba.green, 255)
        self.assertEqual(rgba.blue, 0)
        self.assertEqual(rgba.alpha, 255)
    
    def test_argb(self):
        data = b'\xFF\x00\xFF\x00'
        buffer = ExtendedBuffer(data)
        argb = ARGB.from_buffer(buffer)
        self.assertEqual(argb.red, 0)
        self.assertEqual(argb.green, 255)
        self.assertEqual(argb.blue, 0)
        self.assertEqual(argb.alpha, 255)
    
    def test_color_transform(self):
        # 1 1 0100 1111 1111 1111 0001 0001 0001
        # T T    4   -1   -1   -1    1    1    1
        # 11010011 11111111 11000100 01000100
        #     0xD3     0xFF     0xC4     0x44
        data = b'\xD3\xFF\xC4\x44'
        buffer = ExtendedBuffer(data)
        color_transform = CxForm.from_buffer(buffer)
        self.assertEqual(color_transform.RedMultTerm, -1)
        self.assertEqual(color_transform.GreenMultTerm, -1)
        self.assertEqual(color_transform.BlueMultTerm, -1)
        self.assertEqual(color_transform.RedAddTerm, 1)
        self.assertEqual(color_transform.GreenAddTerm, 1)
        self.assertEqual(color_transform.BlueAddTerm, 1)
    
    def test_color_transform_alpha(self):
        # 1 1 0100 1111 1111 1111 1111 0001 0001 0001 0001
        # T T    4   -1   -1   -1   -1    1    1    1    1
        # 11010011 11111111 11111100 01000100 01000100
        #     0xD3     0xFF     0xFC     0x44     0x44
        data = b'\xD3\xFF\xFC\x44\x44'
        buffer = ExtendedBuffer(data)
        color_transform = CxFormAlpha.from_buffer(buffer)
        self.assertEqual(color_transform.RedMultTerm, -1)
        self.assertEqual(color_transform.GreenMultTerm, -1)
        self.assertEqual(color_transform.BlueMultTerm, -1)
        self.assertEqual(color_transform.AlphaMultTerm, -1)
        self.assertEqual(color_transform.RedAddTerm, 1)
        self.assertEqual(color_transform.GreenAddTerm, 1)
        self.assertEqual(color_transform.BlueAddTerm, 1)
        self.assertEqual(color_transform.AlphaAddTerm, 1)
