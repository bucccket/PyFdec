import xml.etree.cElementTree as ET

from pyfdec.tags.DefineShape import DefineShape


class SvgExporter:
    svg = ET.Element("svg")

    class Cursor:
        x: float = 0
        y: float = 0

        def move(self, dx: float, dy: float):
            self.x += dx / 20
            self.y += dy / 20
        
        def place(self, x:float, y:float):
            self.x = x/20
            self.y = y/20

    def populateSvgHeader(self):
        self.svg.attrib["version"] = "1.1"
        self.svg.attrib["xmlns"] = "http://www.w3.org/2000/svg"

    def __init__(self, defineShapeTag: DefineShape):
        self.populateSvgHeader()
        viewport = defineShapeTag.shapeBounds
        self.svg.attrib["width"] = f"{viewport.xmax/20}"
        self.svg.attrib["height"] = f"{viewport.ymax/20}"
        self.svg.attrib["viewBox"] = (
            f"{viewport.xmin/20} {viewport.ymin/20} {viewport.xmax/20} {viewport.ymax/20}"
        )

        path = ET.SubElement(self.svg, "path")
        path.attrib["d"] = ""
        # NOTE: these arrays are 1 indexed for some fucking reason
        fillstyles: list[DefineShape.ShapeWithStyle.FillStyleArray.FillStyle] = (
            defineShapeTag.shapes.fillStyleArray.fillStyles
        )
        linestyles: list[DefineShape.ShapeWithStyle.LineStyleArray.LineStyle] = (
            defineShapeTag.shapes.lineStyleArray.lineStyles
        )

        # TODO: track cursor position
        cursor: self.Cursor = self.Cursor()

        for shapeRecord in defineShapeTag.shapes.shapeRecords:
            match shapeRecord:
                case DefineShape.ShapeWithStyle.StyleChangeRecord():
                    if shapeRecord.newFillStyleArray:
                        fillstyles += shapeRecord.newFillStyleArray.fillStyles
                    if shapeRecord.fillStyle1:
                        if path.attrib["d"] != "":
                            path.attrib["d"] += "z"
                            path = ET.SubElement(self.svg, "path")
                            path.attrib["d"] = ""
                        fillstyle = fillstyles[shapeRecord.fillStyle1 - 1]
                        if fillstyle.color is not None:
                            path.attrib["fill"] = fillstyle.color.toHexString()
                    if shapeRecord.moveDeltaX is not None:
                        cursor.place(shapeRecord.moveDeltaX, shapeRecord.moveDeltaY)
                        path.attrib[
                            "d"
                        ] += f"m{cursor.x} {cursor.y}"
                    # TODO: implement all other cases
                    pass
                case DefineShape.ShapeWithStyle.StraightEdgeRecord():
                    if shapeRecord.deltaX != 0 and shapeRecord.deltaY != 0:
                        path.attrib[
                            "d"
                        ] += f"l{shapeRecord.deltaX/20} {shapeRecord.deltaY/20}"
                    elif shapeRecord.deltaX != 0:
                        path.attrib["d"] += f"h{shapeRecord.deltaX/20}"
                    else:
                        path.attrib["d"] += f"v{shapeRecord.deltaY/20}"
                case DefineShape.ShapeWithStyle.CurvedEdgeRecord():
                    # TODO: oh my fcking god
                    pass
                case DefineShape.ShapeWithStyle.EndShapeRecord():
                    path.attrib["d"] += "z"

    def getSvgString(self) -> str:
        return ET.tostring(self.svg, encoding="UTF-8")

    def getSvgTree(self) -> ET.ElementTree:
        return ET.ElementTree(self.svg)
