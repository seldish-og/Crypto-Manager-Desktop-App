from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen, QPixmap
import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
from .models import Line
from .models import Candle
from decimal import Decimal
import math

def BestTick(largest, mostticks):
    minimum = largest / mostticks
    magnitude = 10 ** math.floor(math.log(minimum, 10))
    residual = minimum / magnitude
    if residual > 5:
        tick = 10 * magnitude
    elif residual > 2:
        tick = 5 * magnitude
    elif residual > 1:
        tick = 2 * magnitude
    else:
        tick = magnitude
    return tick

import numpy as np

def create_ticks(lo,hi):
    s = 10**(np.floor(np.log10(hi - lo)))
    start = s * np.floor(lo / s)
    end = s * np.ceil(hi / s)
    ticks = [start]
    t = start
    while (t <  end):
        ticks += [t]
        t = t + s
        
    return ticks


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

    def __init__(self, painter) -> None:
        self.painter = painter
        self.height = painter.device().height()
        self.width = painter.device().width()

    def setMaxMinValue(self, data) -> None:
        minimum = float('inf')
        maximum = float('-inf')

        for vertex in data:

            vertex = vertex.__dict__

            for vertex_field in vertex.keys():
                if float(vertex.get(vertex_field)) < minimum:
                    minimum = vertex.get(vertex_field)
                if float(vertex.get(vertex_field)) > maximum:
                    maximum = vertex.get(vertex_field)

        self.maximalValue = maximum
        self.minimalValue = minimum
        self.maxMinDifference = maximum - minimum

    def getVerticalPosition(self, price) -> float:
        return self.height - ChartPositioner.paddingVertical - (self.maxMinDifference - (self.maximalValue - price)) / self.maxMinDifference * (self.height - 2 * ChartPositioner.paddingVertical)


class ChartPositioner:
    paddingVertical = 60
    paddingHorizontal = 100

    @staticmethod
    def setPaddingVertical(padding) -> None:
        ChartPositioner.paddingVertical = padding

    @staticmethod
    def setPaddingHorizontal(padding) -> None:
        ChartPositioner.paddingHorizontal = padding


class LimitDrawer(Drawer):

    def __init__(self, painter) -> None:
        super().__init__(painter)
        pass

    @staticmethod
    def getVertexesAmount(vertexes, width, screenWidth) -> int:
        if (len(vertexes) > screenWidth // width + 1):
            return screenWidth // width + 1
        else:
            return int(len(vertexes))


class GridDrawer(LimitDrawer):
    def __init__(self, painter: QPainter) -> None:
        super().__init__(painter)

        self.minimalGridHeight = 40

        self.gridAmount = self.height // self.minimalGridHeight

    def draw(self, data):
        self.setMaxMinValue(data)

        middlePrice = (self.maximalValue + self.minimalValue) / 2
        minimalCellHeight = 60

        cellAmount = self.height // minimalCellHeight

        grid = np.linspace(self.minimalValue, self.maximalValue, cellAmount)

        for line in grid:
            pen = QPen(QColor(204, 204, 204, 50), 1)
            self.painter.setPen(pen)
            self.painter.drawLine(
                0,
                self.getVerticalPosition(line),
                self.width,
                self.getVerticalPosition(line),
            )
            text = str(line)
            font = QFont("times", 8)
            fm = QFontMetrics(font)
            pen = QPen(QColor("#fff"), 2)
            self.painter.setPen(pen)
            self.painter.setFont(font)
            self.painter.drawText(self.width - fm.width(text),
                                (self.getVerticalPosition(line) - fm.height() / 2), text)



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
        data = data[0:vertexes_amount]
        self.setMaxMinValue(data)
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
                self.drawLine(data[0])
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
        data = data[0:vertexes_amount]
        self.setMaxMinValue(data)

        for i in range(0, vertexes_amount):
            if (i == 0):
                self.drawLine(data[0])

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

        if (self.states.get("positions") is not None):
            for position in self.states["positions"]:
                if (position not in ChartPositioner.__dict__):
                    raise Exception("Unexpected field: " + position)
                setattr(ChartPositioner, position,
                        self.states["positions"][position])

        try:
            self.states["drawers"]
        except Exception:
            raise Exception("There is not enough state: drawers")

        for drawer in self.states["drawers"]:
            try:
                drawer(painter).draw(Chartilo.data)
            except Exception:
                raise Exception(
                    "There is unexpected drawer: " + str(drawer.__name__))

        painter.end()

    def updateCanvas(self):
        self.update()

    def setData(self, data):
        Chartilo.data = VertexesFactory().createVertexes(data)

    def setStates(self, states):
        self.states = states
