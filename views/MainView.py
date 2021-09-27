from threading import local
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen, QPixmap
from models.Line import Line
import sys
import time

from PyQt5.QtWidgets import QApplication, QBoxLayout, QMainWindow, QVBoxLayout, QWidget
from res.dist.templates.Chart import Ui_MainWindow as Chart
# from controllers.ChartController import ChartController


class GridDrawer:
    def __init__(self, painter: QPainter) -> None:
        self.painter = painter

        self.height = painter.device().height()
        self.width = painter.device().width()

        self.minimalGridHeight = 40

        self.gridAmount = self.height // self.minimalGridHeight

        self.paddingVertical = self.height / 10 

        self.paddingHorizontal = self.width / 8

    def calculateVerticalProsition(self, price):
        if not price:
            print("Хъюснат у нас потеря цены")
            return

        return self.height - self.paddingVertical - (self.maxMinDifference - (self.maximalValue - price)) / self.maxMinDifference * (self.height - 2 * self.paddingVertical)

    def getMaxMinValue(self, data, amount=0):
        if (amount == 0):
            amount = len(data)
        minimum = float('inf')
        maximum = float('-inf')

        counter = 0
        for vertex in data:
            if (counter >= amount):
                break

            vertex = vertex.__dict__

            for vertex_field in vertex.keys():
                if float(vertex.get(vertex_field)) < minimum:
                    minimum = vertex.get(vertex_field)
                if float(vertex.get(vertex_field)) > maximum:
                    maximum = vertex.get(vertex_field)

            counter += 1

        self.maximalValue = maximum
        self.minimalValue = minimum
        self.maxMinDifference = maximum - minimum

    def getVertexWidth(self, vertex):
        return vertex.width

    def getVertexesAmount(self, vertexes, width) -> int:
        if (len(vertexes) > (self.width - self.paddingHorizontal) // width + 1):
            return int((self.width - self.paddingHorizontal) // width + 1)
        else:
            return int(len(vertexes))

    def draw(self, data):
        self.getMaxMinValue(data)


class LineChartDrawer(GridDrawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)

    def drawLine(self, vertex):
        pen = QPen(QColor(204, 204, 204, 50), 1, QtCore.Qt.DashLine)
        self.painter.setPen(pen)
        self.painter.drawLine(
            0,
            self.calculateVerticalProsition(vertex.closePrice),
            self.width,
            self.calculateVerticalProsition(vertex.closePrice),
        )
        text = str(vertex.closePrice)
        font = QFont("times", 12)
        fm = QFontMetrics(font);
        pen = QPen(QColor("#fff"), 3)
        self.painter.setPen(pen)
        self.painter.setFont(font)
        self.painter.drawText(self.width - fm.width(text), (self.calculateVerticalProsition(vertex.closePrice) - fm.height() / 2), text);

    def draw(self, data):
        vertexes_amount = self.getVertexesAmount(data, self.getVertexWidth(data[0]))
        self.getMaxMinValue(data, vertexes_amount)

        for i in range(1, vertexes_amount):
            pen = QPen(QColor("#00D3FF"), 3)
            self.painter.setPen(pen)

            self.painter.drawLine(
                self.width - self.paddingHorizontal - i * data[i].width,
                self.calculateVerticalProsition(data[i].openPrice),
                self.width - self.paddingHorizontal - (i - 1) * data[i].width,
                self.calculateVerticalProsition(data[i].closePrice),
            )

            if (i == 1):
                self.drawLine(data[0])


class CandleChartDrawer(LineChartDrawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)

    def draw(self, data):

        vertexes_amount = self.getVertexesAmount(data, self.getVertexWidth(data[0]))
        self.getMaxMinValue(data, vertexes_amount)

        for i in range(0, vertexes_amount):
            if (i == 0):
                self.drawLine(data[0])

            pen = QPen(QColor("#26a69a"), data[i].width - 2)

            if (data[i].openPrice > data[i].closePrice):
                pen = QPen(QColor("#ef5350"), data[i].width - 2)

            self.painter.setPen(pen)

            self.painter.drawLine(
                self.width - self.paddingHorizontal - i * data[i].width,
                self.calculateVerticalProsition(data[i].openPrice),
                self.width - self.paddingHorizontal - (i) * data[i].width,
                self.calculateVerticalProsition(data[i].closePrice),
            )

            pen.setWidth(1)
            self.painter.setPen(pen)

            self.painter.drawLine(
                self.width - self.paddingHorizontal - i * data[i].width,
                self.calculateVerticalProsition(data[i].minimalPrice),
                self.width - self.paddingHorizontal - i * data[i].width,
                self.calculateVerticalProsition(data[i].maximalPrice),
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
        painter = QPainter();
        painter.begin(self);        

        if Canvas.data == None:
            return;

        try:
            self.states["gridDrawer"](painter).draw(Canvas.data)
            self.states["vertexDrawer"](painter).draw(Canvas.data)
        except TypeError:
            raise Exception("Не прилетели у нас состояния")

        painter.end();

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


