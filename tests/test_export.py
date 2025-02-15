import xml.etree.cElementTree as ET
from unittest import TestCase

from pyfdec.extended_buffer import ExtendedBuffer
from pyfdec.swf import Swf
from pyfdec.tags.DefineShape import DefineShape
from pyfdec.util.export.svg_exporter import SvgExporter


class TestExportDefineShape(TestCase):

    def test_exporting_to_svg(self):
        with open('tests/swf/test_Export.swf', 'rb') as file:
            buffer = ExtendedBuffer(file.read())
            swf = Swf.from_buffer(buffer)

            for tag in swf.tags:
                if isinstance(tag, DefineShape):
                    if tag.shapeID == 1:
                        exporter = SvgExporter(tag)
                        svg_string = exporter.getSvgString()
                        self.assertIsNotNone(svg_string)
                        svg = exporter.getSvgTree()
                        svg.write('./test.svg', encoding='UTF-8', xml_declaration=True)

    def test_duplicate_tags(self):
        svg = ET.Element('svg')
        path = ET.SubElement(svg, 'path')
        path.attrib['id'] = '1'
        path = ET.SubElement(svg, 'path')
        path.attrib['id'] = '2'
        svg_string = ET.tostring(svg, encoding='unicode')
        self.assertEqual(svg_string, '<svg><path id="1" /><path id="2" /></svg>')
