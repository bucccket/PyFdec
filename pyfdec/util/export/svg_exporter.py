import xml.etree.cElementTree as ET

from pyfdec.tags.DefineShape import DefineShape


class SvgExporter:
    svg = ET.Element("svg")

    class Cursor:
        _x: float = 0
        _y: float = 0

        @property
        def x(self) -> float:
            return round(self._x, 2)

        @x.setter
        def x(self, value: float):
            self._x = round(value, 2)

        @property
        def y(self) -> float:
            return round(self._y, 2)

        @y.setter
        def y(self, value: float):
            self._y = round(value, 2)

        def moveTwips(self, dx: float, dy: float):
            self.x += dx / 20
            self.y += dy / 20

        def placeTwips(self, x: float, y: float):
            self.x = x / 20
            self.y = y / 20

    def populateSvgHeader(self):
        self.svg.attrib["version"] = "1.1"
        self.svg.attrib["xmlns"] = "http://www.w3.org/2000/svg"

    def _makePath(
        self,
        parent: ET.Element,
        cursor: Cursor,
        color: str,
    ) -> ET.Element:
        path = ET.SubElement(parent, "path")
        path.attrib["d"] = f"M {cursor.x} {cursor.y}"
        path.attrib["fill-rule"] = "evenodd"
        path.attrib["fill"] = color
        return path

    def __init__(self, defineShapeTag: DefineShape):
        self.populateSvgHeader()
        viewport = defineShapeTag.shapeBounds
        self.svg.attrib["width"] = f"{(viewport.xmax-viewport.xmin)/20}px"
        self.svg.attrib["height"] = f"{(viewport.ymax-viewport.ymin)/20}px"

        g = ET.SubElement(self.svg, "g")
        g.attrib["transform"] = (
            f"matrix(1.0, 0.0, 0.0, 1.0, {-viewport.xmin/20}, {-viewport.ymin/20})"
        )

        fillstyles: list[DefineShape.ShapeWithStyle.FillStyleArray.FillStyle] = (
            defineShapeTag.shapes.fillStyleArray.fillStyles
        )
        linestyles: list[DefineShape.ShapeWithStyle.LineStyleArray.LineStyle] = (
            defineShapeTag.shapes.lineStyleArray.lineStyles
        )

        # TODO: track cursor position
        cursor: SvgExporter.Cursor = SvgExporter.Cursor()

        # TODO: track path0 and path1 separately and apply all modifications to both
        paths: dict[str, ET.Element] = {}
        path0 = None
        path1 = None

        #TODO: make intermediary helper class that treats path sections seperately
        # FIXME: paths MUST start with moveto
        # FIXME: enforce grouping all nodes by color instead of generating new paths for each color change
        # NOTE: absolute coords are used since the way paths are traversed is not guaranteed to be continuous
        for shapeRecord in defineShapeTag.shapes.shapeRecords:
            match shapeRecord:
                case DefineShape.ShapeWithStyle.StyleChangeRecord():
                    if shapeRecord.newFillStyleArray:
                        fillstyles = shapeRecord.newFillStyleArray.fillStyles
                    # TODO: split this to path0 and path1
                    if shapeRecord.fillStyle0 is not None:
                        if shapeRecord.fillStyle0 > 0:
                            fillstyle = fillstyles[shapeRecord.fillStyle0 - 1]
                            color = fillstyle.color.toHexString()
                            if color not in paths:
                                path0 = self._makePath(g, cursor, color)
                                paths[color] = path0
                            else:
                                path0 = paths[color]
                        else:
                            path0 = None
                    if shapeRecord.fillStyle1 is not None:
                        if shapeRecord.fillStyle1 > 0:
                            fillstyle = fillstyles[shapeRecord.fillStyle1 - 1]
                            color = fillstyle.color.toHexString()
                            if color not in paths:
                                path1 = self._makePath(g, cursor, color)
                                paths[color] = path1
                            else:
                                path1 = paths[color]
                        else:
                            path1 = None
                    if shapeRecord.moveDeltaX is not None:
                        cursor.placeTwips(
                            shapeRecord.moveDeltaX, shapeRecord.moveDeltaY
                        )
                        if path0 is not None:
                            path0.attrib["d"] += f"M{cursor.x} {cursor.y}"
                        if path1 is not None:
                            path1.attrib["d"] += f"M{cursor.x} {cursor.y}"
                    # TODO: implement all other cases
                    pass
                case DefineShape.ShapeWithStyle.StraightEdgeRecord():
                    dx = round(cursor.x + shapeRecord.deltaX / 20, 2)
                    dy = round(cursor.y + shapeRecord.deltaY / 20, 2)
                    if shapeRecord.deltaX != 0 and shapeRecord.deltaY != 0:
                        if path0 is not None:
                            path0.attrib["d"] += f"L{dx} {dy}"
                        if path1 is not None:
                            path1.attrib["d"] += f"L{dx} {dy}"
                    elif shapeRecord.deltaX != 0:
                        if path0 is not None:
                            path0.attrib["d"] += f"H{dx}"
                        if path1 is not None:
                            path1.attrib["d"] += f"H{dx}"
                    else:
                        if path0 is not None:
                            path0.attrib["d"] += f"V{dy}"
                        if path1 is not None:
                            path1.attrib["d"] += f"V{dy}"
                    cursor.moveTwips(shapeRecord.deltaX, shapeRecord.deltaY)
                case DefineShape.ShapeWithStyle.CurvedEdgeRecord():
                    controlX = round(cursor.x + shapeRecord.controlDeltaX / 20, 2)
                    controlY = round(cursor.y + shapeRecord.controlDeltaY / 20, 2)
                    cursor.moveTwips(
                        shapeRecord.controlDeltaX, shapeRecord.controlDeltaY
                    )
                    cursor.moveTwips(shapeRecord.anchorDeltaX, shapeRecord.anchorDeltaY)
                    if path0 is not None:
                        path0.attrib[
                            "d"
                        ] += f"Q{controlX} {controlY} {cursor.x} {cursor.y}"
                    if path1 is not None:
                        path1.attrib[
                            "d"
                        ] += f"Q{controlX} {controlY} {cursor.x} {cursor.y}"
                case DefineShape.ShapeWithStyle.EndShapeRecord():
                    for path in paths.values():
                        path.attrib["d"] += "Z"

    def getSvgString(self) -> str:
        return ET.tostring(self.svg, encoding="UTF-8")

    def getSvgTree(self) -> ET.ElementTree:
        return ET.ElementTree(self.svg)
