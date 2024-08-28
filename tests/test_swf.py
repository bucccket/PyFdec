from unittest import TestCase

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.record_types.geometric_types import Rect
from pyfdec.swf.swf_file import SwfFile, SwfHeader
from pyfdec.tags.DefineShape import DefineShape
from pyfdec.tags.DefineSprite import DefineSprite
from pyfdec.tags.DoABC import DoABC
from pyfdec.tags.Tag import Tag


class TestSwfHeader(TestCase):
    def test_reading_swf_header(self):
        with open("tests/swf/Gfx_Ahsoka_Sword.swf", "rb") as file:
            buffer = ExtendedBuffer(file.read())
            swf_header, buffer = SwfHeader.from_buffer(buffer)
            self.assertEqual(swf_header.compression, SwfHeader.CompressionLevel.NONE)
            self.assertEqual(swf_header.version, 15)
            self.assertEqual(swf_header.fileLength, 17980)
            self.assertEqual(swf_header.frameCount, 1)
            self.assertEqual(swf_header.frameRate, 24.0)
            self.assertEqual(swf_header.frameSize, Rect(0, 11000, 0, 8000))


class TestSwfFile(TestCase):
    def test_reading_swf_file(self):
        with open("tests/swf/test_DefineShape.swf", "rb") as file:
            buffer = ExtendedBuffer(file.read())
            swf = SwfFile.from_buffer(buffer)
            self.assertFalse(swf.fileAttributes.useDirectBlit)
            self.assertFalse(swf.fileAttributes.useGPU)
            self.assertFalse(swf.fileAttributes.hasMetadata)
            self.assertTrue(swf.fileAttributes.actionScript3)
            self.assertFalse(swf.fileAttributes.noCrossDomainCaching)
            self.assertFalse(swf.fileAttributes.useNetwork)

            for tag in swf.tags:
                self.assertTrue(isinstance(tag, Tag))
                if isinstance(tag, DefineSprite):
                    for sprite_tag in tag.tags:
                        self.assertTrue(isinstance(sprite_tag, Tag))
                elif isinstance(tag, DefineShape):
                    for shaperecord in tag.shapes.shapeRecords:
                        self.assertTrue(
                            isinstance(
                                shaperecord, DefineShape.ShapeWithStyle.ShapeRecord
                            )
                        )

    def test_reading_bhair(self):
        # brawlhalla air version: 8.12
        with open("tests/swf/BrawlhallaAir.swf", "rb") as file:
            buffer = ExtendedBuffer(file.read())
            swf = SwfFile.from_buffer(buffer)
            self.assertEqual(swf.header.compression, SwfHeader.CompressionLevel.ZLIB)
            abc_tag: DoABC = [
                tag for tag in swf.tags if tag.tag_type == tag.TagTypes.DoABC
            ][0]
            self.assertEqual(len(abc_tag.ABCData.cpool.ints), 864)
            self.assertEqual(len(abc_tag.ABCData.cpool.uints), 214)
            self.assertEqual(len(abc_tag.ABCData.cpool.doubles), 644)
            self.assertEqual(len(abc_tag.ABCData.cpool.strings), 33138)
            self.assertEqual(len(abc_tag.ABCData.cpool.namespaces), 35)
            self.assertEqual(len(abc_tag.ABCData.cpool.namespace_sets), 3)
            self.assertEqual(len(abc_tag.ABCData.cpool.multinames), 23870)
            self.assertEqual(len(abc_tag.ABCData.methods), 12095)
            self.assertEqual(len(abc_tag.ABCData.metadata), 0)
            self.assertEqual(len(abc_tag.ABCData.classes), 641)
            self.assertEqual(len(abc_tag.ABCData.scripts), 641)
            self.assertEqual(len(abc_tag.ABCData.method_bodies), 12046)
