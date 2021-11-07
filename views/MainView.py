from lib import Chartilo

from PyQt5.QtWidgets import QApplication, QBoxLayout, QMainWindow, QVBoxLayout, QWidget
from res.dist.templates.Chart import Ui_MainWindow as Chart


class MainView(QMainWindow):

    def __init__(self):
        super(MainView, self).__init__()
        self.chart = Chart()
        self.chart.setupUi(self)
        self.showMaximized()
        self.createCanvas()

    def createCanvas(self):
        self._chartilo = Chartilo()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._chartilo)
        self.chart.chartFrame.setLayout(layout)

    def updateCanvas(self):
        self._chartilo.updateCanvas()

    def setCanvasData(self, data):
        self._chartilo.setData(data)

    def setCanvasStates(self, states):
        self._chartilo.setStates(states)
