from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QPen, QPixmap
from models.Line import Line
import sys


from PyQt5.QtWidgets import QApplication, QMainWindow
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
        self.painter = painter
        pass

    def runLoader(self):
        self.painter


class MainView(QMainWindow):

    def __init__(self):
        super(MainView, self).__init__()
        self.chart = Chart()
        self.chart.setupUi(self)
        self.showMaximized()

    def createPainter(self):
        screen = QApplication.primaryScreen()
        print(screen.size())
        self.pixmap = QPixmap(self.chart.drawLabel.size())
        self.pixmap = self.pixmap.scaledToHeight(screen.size().height())
        self.pixmap = self.pixmap.scaledToWidth(screen.size().width())
        self.pixmap.fill(QtCore.Qt.transparent)
        self.painter = QPainter(self.pixmap)
        print(self.pixmap.width())
        print(self.chart.drawLabel.frameGeometry().width())

    def closePainter(self):
        self.painter.end()

    def setPainter(self):
        self.chart.drawLabel.setPixmap(self.pixmap)

    def clearPainter(self):
        self.chart.drawLabel.clear()
