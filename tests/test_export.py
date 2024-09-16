from unittest import TestCase

import xml.etree.cElementTree as ET

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.swf.swf_file import SwfFile
from pyfdec.tags.DefineShape import DefineShape
from pyfdec.tags.DefineSprite import DefineSprite
from pyfdec.tags.Tag import Tag
from pyfdec.util.export.svg_exporter import SvgExporter


class TestExportDefineShape(TestCase):
    def test_exporting_to_svg(self):
        with open("tests/swf/test_DefineShape.swf", "rb") as file:
            buffer = ExtendedBuffer(file.read())
            swf = SwfFile.from_buffer(buffer)

            for tag in swf.tags:
                if isinstance(tag, DefineShape):
                    if tag.shapeID == 7:
                        exporter = SvgExporter(tag)
                        svg_string = exporter.getSvgString()
                        self.assertIsNotNone(svg_string)
                        svg = exporter.getSvgTree()
                        svg.write("test.svg")

    def test_duplicate_tags(self):
        svg = ET.Element("svg")
        path = ET.SubElement(svg, "path")
        path.attrib["id"] = "1"
        path = ET.SubElement(svg, "path")
        path.attrib["id"] = "2"
        svg_string = ET.tostring(svg, encoding="unicode")
        self.assertEqual(svg_string, '<svg><path id="1" /><path id="2" /></svg>')
