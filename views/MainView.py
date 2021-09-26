from threading import local
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QPixmap
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

        self.paddingVertical = self.height / 8

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
        if (len(vertexes) > self.width // width):
            return self.width // width
        else:
            return len(vertexes)

    def draw(self, data):
        self.getMaxMinValue(data)


class LineChartDrawer(GridDrawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)

    def draw(self, data):

        vertexes_amount = self.getVertexesAmount(
            data, self.getVertexWidth(data[0]))
        self.getMaxMinValue(data)

        for i in range(0, vertexes_amount):
            pen = QPen(QtCore.Qt.red, 3)
            self.painter.setPen(pen)
            self.painter.drawLine(
                self.width - i * data[i].width,
                self.calculateVerticalProsition(data[i].openPrice),
                self.width - (i - 1) * data[i].width,
                self.calculateVerticalProsition(data[i].closePrice),
            )


class CandleChartDrawer(LineChartDrawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)


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

        GridDrawer(painter).draw(Canvas.data)
        LineChartDrawer(painter).draw(Canvas.data)

        painter.end();

    def updateCanvas(self):
        self.update()

    def setData(self, data):
        Canvas.data = data


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
        layout.addWidget(self._canvas)
        self.chart.chartFrame.setLayout(layout)

    def updateCanvas(self):
        self._canvas.updateCanvas()
    
    def setCanvasData(self, data):
        self._canvas.setData(data)


