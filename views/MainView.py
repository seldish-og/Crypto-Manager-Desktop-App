from threading import local
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen, QPixmap
from models.Line import Line
import sys
import time

from PyQt5.QtWidgets import QApplication, QBoxLayout, QMainWindow, QVBoxLayout, QWidget
from res.dist.templates.Chart import Ui_MainWindow as Chart
# from controllers.ChartController import ChartController


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
        pass


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
        vertexes_amount = self.getVertexesAmount(data, 7, self.width - ChartPositioner.paddingHorizontal)
        data = data[0:vertexes_amount]
        self.setMaxMinValue(data)
        print(self.maximalValue, self.minimalValue)

        for i in range(0, vertexes_amount - 1):
            pen = QPen(QColor("#00D3FF"), 3)
            self.painter.setPen(pen)

            if (i == 0):
                self.painter.drawLine(
                    self.width - ChartPositioner.paddingHorizontal - (i) * 7,
                    self.getVerticalPosition(data[i].closePrice),
                    self.width - ChartPositioner.paddingHorizontal - (i + 1) * 7,
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
        vertexes_amount = self.getVertexesAmount(data, data[0].width, self.width)
        data = data[0:vertexes_amount]
        self.setMaxMinValue(data)

        for i in range(0, vertexes_amount):
            if (i == 0):
                self.drawLine(data[0])

            pen = QPen(QColor("#26a69a"), data[i].width - 2)

            if (data[i].openPrice > data[i].closePrice):
                pen = QPen(QColor("#ef5350"), data[i].width - 2)

            self.painter.setPen(pen)

            self.painter.drawLine(
                self.width - ChartPositioner.paddingHorizontal - i * data[i].width,
                self.getVerticalPosition(data[i].openPrice),
                self.width - ChartPositioner.paddingHorizontal - (i) * data[i].width,
                self.getVerticalPosition(data[i].closePrice),
            )

            pen.setWidth(1)
            self.painter.setPen(pen)

            self.painter.drawLine(
                self.width - ChartPositioner.paddingHorizontal - i * data[i].width,
                self.getVerticalPosition(data[i].minimalPrice),
                self.width - ChartPositioner.paddingHorizontal - i * data[i].width,
                self.getVerticalPosition(data[i].maximalPrice),
            )


class Loader:
    def __init__(self, painter) -> None:
        self._painter = painter
        pass

    def runLoader(self):
        self._painter


class Canvas(QWidget):
    data = None

    def __init__(self) -> None:
        super(Canvas, self).__init__()

    def paintEvent(self, event) -> None:
        painter = QPainter()
        painter.begin(self)

        if Canvas.data == None:
            return

        try:
            self.states["gridDrawer"](painter).draw(Canvas.data)
            self.states["vertexDrawer"](painter).draw(Canvas.data)
        except TypeError:
            raise Exception("Не прилетели у нас состояния")

        painter.end()

    def updateCanvas(self):
        self.update()

    def setData(self, data):
        Canvas.data = data

    def setStates(self, states):
        self.states = states


class MainView(QMainWindow):

    def __init__(self):
        super(MainView, self).__init__()
        self.chart = Chart()
        self.chart.setupUi(self)
        self.showMaximized()
        self.createCanvas()

    def createCanvas(self):
        self._canvas = Canvas()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self._canvas.setContentsMargins(0, 0, 0, 0)
        self.chart.chartFrame.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._canvas)
        self.chart.chartFrame.setLayout(layout)

    def updateCanvas(self):
        self._canvas.updateCanvas()

    def setCanvasData(self, data):
        self._canvas.setData(data)

    def setCanvasStates(self, states):
        self._canvas.setStates(states)
