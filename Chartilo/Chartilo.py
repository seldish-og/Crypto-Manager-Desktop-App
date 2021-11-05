import bisect
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen, QPixmap
import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
from .models import Line
from .models import Candle
from decimal import Decimal
import math


class NiceScale:
    def __init__(self, minv, maxv):
        self.maxTicks = 6
        self.tickSpacing = 0
        self.lst = 10
        self.niceMin = 0
        self.niceMax = 0
        self.minPoint = minv
        self.maxPoint = maxv
        self.calculate()

    def calculate(self):
        self.lst = self.niceNum(self.maxPoint - self.minPoint, False)
        self.tickSpacing = self.niceNum(
            self.lst / (self.maxTicks - 1), True)
        self.niceMin = math.floor(
            self.minPoint / self.tickSpacing) * self.tickSpacing
        self.niceMax = math.ceil(Decimal(str(
            self.maxPoint)) / Decimal(str(self.tickSpacing))) * Decimal(str(self.tickSpacing))

    def niceNum(self, lst, rround):
        self.lst = lst
        exponent = 0  # exponent of range */
        fraction = 0  # fractional part of range */
        niceFraction = 0  # nice, rounded fraction */

        exponent = math.floor(math.log10(self.lst))
        fraction = self.lst / math.pow(10, exponent)

        if (self.lst):
            if (fraction < 1.5):
                niceFraction = 1
            elif (fraction < 3):
                niceFraction = 2
            elif (fraction < 7):
                niceFraction = 5
            else:
                niceFraction = 10
        else:
            if (fraction <= 1):
                niceFraction = 1
            elif (fraction <= 2):
                niceFraction = 2
            elif (fraction <= 5):
                niceFraction = 5
            else:
                niceFraction = 10

        return niceFraction * math.pow(10, exponent)

    def setMinMaxPoints(self, minPoint, maxPoint):
        self.minPoint = minPoint
        self.maxPoint = maxPoint
        self.calculate()

    def setMaxTicks(self, maxTicks):
        self.maxTicks = maxTicks
        self.calculate()


class VertexesFactory:
    Type = Line

    def __init__(self) -> None:
        self.newVertexes = []

    def createVertex(self, vertex):
        return type(vertex)

    def createVertexes(self, vertexes):
        for i in vertexes:
            self.newVertexes.append(VertexesFactory.Type(i))
        return self.newVertexes


class Drawer:
    maximalValue = 0
    minimalValue = 0
    maxMinDifference = 0

    def __init__(self, painter) -> None:
        self.painter = painter
        self.height = painter.device().height()
        self.width = painter.device().width()

    @staticmethod
    def setMaxMinValue(data) -> None:
        minimum = float('inf')
        maximum = float('-inf')

        for vertex in data:

            vertex = vertex.__dict__

            for vertex_field in vertex.keys():
                if float(vertex.get(vertex_field)) < minimum:
                    minimum = vertex.get(vertex_field)
                if float(vertex.get(vertex_field)) > maximum:
                    maximum = vertex.get(vertex_field)

        Drawer.maximalValue = maximum
        Drawer.minimalValue = minimum
        Drawer.maxMinDifference = maximum - minimum

    def getVerticalPosition(self, price) -> float:
        return self.height - ChartPositioner.paddingVertical - (Drawer.maxMinDifference - (Drawer.maximalValue - price)) / Drawer.maxMinDifference * (self.height - 2 * ChartPositioner.paddingVertical)


class ChartPositioner:
    paddingVertical = 120
    paddingHorizontal = 71

    @staticmethod
    def setPaddingVertical(padding) -> None:
        ChartPositioner.paddingVertical = padding

    @staticmethod
    def setPaddingHorizontal(padding) -> None:
        ChartPositioner.paddingHorizontal = padding


class LimitDrawer(Drawer):
    drawableData = []

    def __init__(self, painter) -> None:
        super().__init__(painter)
        pass

    @staticmethod
    def getVertexesAmount(vertexes, vertexWidth, screenWidth, horizontalMargin=0) -> int:
        localMargin = horizontalMargin
        if (localMargin < 0):
            localMargin = 0

        if (len(vertexes) > (screenWidth - horizontalMargin) // vertexWidth + 1):
            return screenWidth // vertexWidth + 1
        else:
            return int(len(vertexes))

    @staticmethod
    def setDrawableData(data):
        LimitDrawer.drawableData = data

    @staticmethod
    def calculateDrawableData(data, startPosition, endPosition):
        return data[startPosition:endPosition]


class GridDrawer(LimitDrawer):
    def __init__(self, painter: QPainter) -> None:
        super().__init__(painter)

        self.minimalGridHeight = 40

        self.gridAmount = self.height // self.minimalGridHeight

    def draw(self, data):
        print("Grid drawer:", Drawer.maximalValue, Drawer.minimalValue)

        gridSettings = NiceScale(Drawer.minimalValue, Drawer.maximalValue)
        # print("a.lst ", gridSettings.lst)
        # print("a.maxPoint ", gridSettings.maxPoint)
        # print("a.maxTicks ", gridSettings.maxTicks)
        # print("a.minPoint ", gridSettings.minPoint)
        # print("a.niceMax ", gridSettings.niceMax)
        # print("a.niceMin ", gridSettings.niceMin)
        # print("a.tickSpacing ", gridSettings.tickSpacing)

        maximalLength = len(str(Decimal(Drawer.maximalValue) % 1)[:2])

        grid = []
        for i in range(gridSettings.maxTicks + 1):
            grid.append(float(Decimal(str(gridSettings.niceMin)) +
                        Decimal(str(i)) * Decimal(str(gridSettings.tickSpacing))))

        for i in grid:
            if (len(str(Decimal(str(i)) % 1)) - 2 > maximalLength):
                maximalLength = len(str(Decimal(str(i)) % 1)) - 2

        for i in grid:
            pen = QPen(QColor(204, 204, 204, 50), 1)
            self.painter.setPen(pen)
            self.painter.drawLine(
                0,
                self.getVerticalPosition(i),
                self.width,
                self.getVerticalPosition(i),
            )
            text = str(("{0:." + str(maximalLength) + "f}").format(i))
            font = QFont("times", 8)
            fm = QFontMetrics(font)
            pen = QPen(QColor("#fff"), 2)
            self.painter.setPen(pen)
            self.painter.setFont(font)
            self.painter.drawText(self.width - fm.width(text),
                                  (self.getVerticalPosition(i) - fm.height() / 2), text)


class MaxMinValuesDrawer(Drawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)

    def draw(self, data):
        maximalLength = len(str(Decimal(Drawer.maximalValue) % 1)[:2])

        # maximal point
        pen = QPen(QColor("#26a69a"), 0.5)
        self.painter.setPen(pen)
        self.painter.drawLine(
            0,
            self.getVerticalPosition(Drawer.maximalValue),
            self.width,
            self.getVerticalPosition(Drawer.maximalValue),
        )
        text = str(self.maximalValue)
        font = QFont("times", 10)
        fm = QFontMetrics(font)
        pen = QPen(QColor("#26a69a"), 2)
        self.painter.setPen(pen)
        self.painter.setFont(font)
        self.painter.drawText(0, (self.getVerticalPosition(
            Drawer.maximalValue) - fm.height() / 2), text)

        # minimal point
        pen = QPen(QColor("#ef5350"), 0.5)
        self.painter.setPen(pen)
        self.painter.drawLine(
            0,
            self.getVerticalPosition(Drawer.minimalValue),
            self.width,
            self.getVerticalPosition(Drawer.minimalValue),
        )
        text = str(self.minimalValue)
        font = QFont("times", 10)
        fm = QFontMetrics(font)
        pen = QPen(QColor("#ef5350"), 2)
        self.painter.setPen(pen)
        self.painter.setFont(font)
        self.painter.drawText(0, (self.getVerticalPosition(
            self.minimalValue) - fm.height() / 2), text)


class LineDrawer(Drawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)

    def draw(self, data):
        vertex = data[0]
        pen = QPen(QColor(204, 204, 204, 50), 1, QtCore.Qt.DashLine)
        self.painter.setPen(pen)
        self.painter.drawLine(
            0,
            self.getVerticalPosition(vertex.closePrice),
            self.width,
            self.getVerticalPosition(vertex.closePrice),
        )
        text = str(vertex.closePrice)
        font = QFont("times", 12)
        fm = QFontMetrics(font)
        pen = QPen(QColor("#fff"), 3)
        self.painter.setPen(pen)
        self.painter.setFont(font)
        self.painter.drawText(self.width - fm.width(text),
                              (self.getVerticalPosition(vertex.closePrice) - fm.height() / 2), text)


class LineChartDrawer(LimitDrawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)

    def drawLine(self, vertex):
        pen = QPen(QColor(204, 204, 204, 50), 1, QtCore.Qt.DashLine)
        self.painter.setPen(pen)
        self.painter.drawLine(
            0,
            self.getVerticalPosition(vertex.closePrice),
            self.width,
            self.getVerticalPosition(vertex.closePrice),
        )
        text = str(vertex.closePrice)
        font = QFont("times", 12)
        fm = QFontMetrics(font)
        pen = QPen(QColor("#fff"), 3)
        self.painter.setPen(pen)
        self.painter.setFont(font)
        self.painter.drawText(self.width - fm.width(text),
                              (self.getVerticalPosition(vertex.closePrice) - fm.height() / 2), text)

    def draw(self, data):
        vertexes_amount = self.getVertexesAmount(
            data, 7, self.width - ChartPositioner.paddingHorizontal)
        # data = data[0:vertexes_amount]
        print("Line chart drawer: ", Drawer.maximalValue, Drawer.minimalValue)
        # print(self.maximalValue, self.minimalValue)

        for i in range(0, vertexes_amount - 1):
            pen = QPen(QColor("#00D3FF"), 3)
            self.painter.setPen(pen)

            if (i == 0):
                self.painter.drawLine(
                    self.width - ChartPositioner.paddingHorizontal - (i) * 7,
                    self.getVerticalPosition(data[i].closePrice),
                    self.width - ChartPositioner.paddingHorizontal -
                    (i + 1) * 7,
                    self.getVerticalPosition(data[i].openPrice),
                )
                continue

            self.painter.drawLine(
                self.width - ChartPositioner.paddingHorizontal - i * 7,
                self.getVerticalPosition(data[i - 1].openPrice),
                self.width - ChartPositioner.paddingHorizontal - (i + 1) * 7,
                self.getVerticalPosition(data[i].openPrice),
            )


class CandleChartDrawer(LineChartDrawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)

    def draw(self, data):
        vertexes_amount = self.getVertexesAmount(
            data, data[0].width, self.width)
        # data = data[0:vertexes_amount]

        for i in range(0, vertexes_amount):

            pen = QPen(QColor("#26a69a"), data[i].width - 3)

            if (data[i].openPrice > data[i].closePrice):
                pen = QPen(QColor("#ef5350"), data[i].width - 3)

            self.painter.setPen(pen)

            self.painter.drawLine(
                self.width - ChartPositioner.paddingHorizontal -
                i * data[i].width,
                self.getVerticalPosition(data[i].openPrice),
                self.width - ChartPositioner.paddingHorizontal -
                (i) * data[i].width,
                self.getVerticalPosition(data[i].closePrice),
            )

            pen.setWidth(1)
            self.painter.setPen(pen)

            self.painter.drawLine(
                self.width - ChartPositioner.paddingHorizontal -
                i * data[i].width,
                self.getVerticalPosition(data[i].minimalPrice),
                self.width - ChartPositioner.paddingHorizontal -
                i * data[i].width,
                self.getVerticalPosition(data[i].maximalPrice),
            )


class Loader:
    def __init__(self, painter) -> None:
        self._painter = painter
        pass

    def runLoader(self):
        self._painter


class Chartilo(QWidget):
    data = None

    def __init__(self) -> None:
        super(Chartilo, self).__init__()

    def paintEvent(self, event) -> None:
        painter = QPainter()
        painter.begin(self)

        if Chartilo.data == None:
            print("There is no data to draw")
            return

        Drawer.setMaxMinValue(Chartilo.data)

        LimitDrawer.setDrawableData(LimitDrawer.calculateDrawableData(Chartilo.data, 0, LimitDrawer.getVertexesAmount(Chartilo.data, 7, painter.device().width(), ChartPositioner.paddingHorizontal)))

        if (self.states.get("positions") is not None):
            for position in self.states["positions"]:
                if (position not in ChartPositioner.__dict__):
                    raise Exception("Unexpected field: " + position)
                setattr(ChartPositioner, position,
                        self.states["positions"][position])

        try:
            self.states["drawers"]
        except Exception as e:
            raise Exception(e + "\nThere is not enough state: drawers")

        for drawer in self.states["drawers"]:
            try:
                self.states["drawers"][drawer](painter).draw(LimitDrawer.drawableData)
            except Exception as e:
                raise Exception(str(e) +
                                "\nThere is unexpected drawer: " + str(drawer))

        painter.end()

    def updateCanvas(self):
        self.update()

    def setData(self, data):
        Chartilo.data = VertexesFactory().createVertexes(data)

    def setStates(self, states):
        self.states = states
