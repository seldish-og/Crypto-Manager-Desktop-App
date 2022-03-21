from chartilo import Chartilo

from PyQt5.QtWidgets import QApplication, QBoxLayout, QMainWindow, QVBoxLayout, QWidget
from res.dist.templates.Chart import Ui_MainWindow as Chart

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget 


class MainView(QMainWindow):

    def __init__(self, controller):
        super(MainView, self).__init__()
        self._controller = controller
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

    def appendSymbols(self, symbols):
        for i in reversed(range(self.chart.appendHere.layout().count())):
            self.chart.appendHere.layout().itemAt(i).widget().setParent(None)

        for symbol in symbols:
            frame = QFrame()
            frame.setObjectName(str(symbol))
            frame.setStyleSheet("padding: 0px; margin: 0px;")
            frame.installEventFilter(self)
            layout = QHBoxLayout()
            label = QLabel(symbol)
            label.setStyleSheet("color: #fff; font-size: 14px; margin: 0px; padding: 0px;")
            layout.addWidget(label)
            frame.setLayout(layout)

            self.chart.appendHere.layout().addWidget(frame)

    def eventFilter(self, obj, event):
        self._controller.changeCurrencySymbol(obj, event)
        return QWidget.eventFilter(self, obj, event)
