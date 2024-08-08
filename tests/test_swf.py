from unittest import TestCase

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.geometric_types import Rect
from pyfdec.swf.swf_file import SwfFile, SwfHeader


class TestSwfHeader(TestCase):
    def test_reading_swf_header(self):
        with open('tests/Gfx_Ahsoka_Sword.swf', 'rb') as file:
            buffer = ExtendedBuffer(file.read())
            swf_header = SwfHeader.from_buffer(buffer)
            self.assertEqual(swf_header.compression,
                             SwfHeader.CompressionLevel.Uncompressed)
            self.assertEqual(swf_header.version, 15)
            self.assertEqual(swf_header.fileLength, 17980)
            self.assertEqual(swf_header.frameCount, 1)
            self.assertEqual(swf_header.frameRate, 24.0)
            self.assertEqual(swf_header.frameSize, Rect(0, 11000, 0, 8000))


class TestSwfFile(TestCase):
    def test_reading_swf_file(self):
        with open('tests/Gfx_Ahsoka_Sword.swf', 'rb') as file:
            buffer = ExtendedBuffer(file.read())
            swf = SwfFile.from_buffer(buffer)