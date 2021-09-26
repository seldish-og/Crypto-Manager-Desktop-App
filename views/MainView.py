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
        # print(self.painter.device().height())
        # print(self.painter.device().width())

    def draw(self, data):
        pass


class LineChartDrawer(GridDrawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)


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

    def createPainter(self):
        self.pixmap = QPixmap(self.chart.drawLabel.size())
        self.pixmap.fill(QtCore.Qt.transparent)
        self.painter = QPainter(self.pixmap)

    def closePainter(self):
        pen = QPen(QtCore.Qt.red, 3)
        self.painter.setPen(pen)
        self.painter.drawLine(10, 10, 50, 50)
        self.painter.end()

    def setPainter(self):
        self.chart.drawLabel.setPixmap(self.pixmap)

    def clearPainter(self):
        self.chart.drawLabel.clear()