from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QPen, QPixmap
from models.Line import Line
import sys


from PyQt5.QtWidgets import QApplication, QMainWindow
from res.dist.templates.Chart import Ui_MainWindow as Chart
# from controllers.ChartController import ChartController

class GridDrawer:
    def __init__(self, canvas) -> None:
        pass

class LineChartDrawer(GridDrawer):
    def __init__(self) -> None:
        super().__init__()


class CandleChartDrawer(LineChartDrawer):
    def __init__(self) -> None:
        super().__init__()
    
class Loader:
    def __init__(self) -> None:
        pass

class MainView(QMainWindow):

    def __init__(self):
        super(MainView, self).__init__()

        self.chart = Chart()
        self.chart.setupUi(self)

        pixmap = QPixmap(self.chart.drawLabel.size())
        pixmap.fill(QtCore.Qt.transparent)
        self.painter = QPainter(pixmap)
        pen = QPen(QtCore.Qt.red, 3)
        self.painter.setPen(pen)
        self.painter.drawLine(10, 10, 50, 50)
        self.painter.end()
        self.chart.drawLabel.setPixmap(pixmap)


        self._drawChart()

    def _drawChart(self):
        # vertexes = self.states["connectionChart"]();
        # print(vertexes)

        print("Ща рисовать будем")
