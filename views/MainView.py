from models.Line import Line
import sys


from PyQt5.QtWidgets import QApplication, QMainWindow
from res.dist.templates.Chart import Ui_MainWindow as Chart
from controllers.ChartController import ChartController
from repository.ChartRepository import ChartRepository

class Grid:
    def __init__(self) -> None:
        pass

class LineChart(Grid):
    def __init__(self) -> None:
        super().__init__()


class CandleChart(LineChart):
    def __init__(self) -> None:
        super().__init__()

class MainView(QMainWindow):

    def __init__(self):
        super(MainView, self).__init__()

        self.chart = Chart()
        self.chart.setupUi(self)

        self.controller = ChartController()

        self._drawChart()

    def _drawChart(self):
        vertexes = self.controller.getChartData();
        print(vertexes)
        print(vertexes[0].openPrice)

        # pixmap = QPixmap(self.drawLable.size())
        # pixmap.fill(QtCore.Qt.transparent)
        # self.drawLable.setPixmap(pixmap)
        # qp = QPainter(pixmap)
        # pen = QPen(QtCore.Qt.red, 3)
        # qp.setPen(pen)
        # qp.drawLine(10, 10, 50, 50)
        # qp.end()
