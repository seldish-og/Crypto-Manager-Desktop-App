import sys
import json
import threading
import time

from PyQt5 import QtCore, QtWidgets
from views.MainView import MainView

from repository.Connection import Connection
from PyQt5.QtGui import QPainter, QPen, QPixmap
from repository.ChartRepository import ChartRepository

from lib.drawers import GridDrawer, LineChartDrawer, MaxMinValuesDrawer, LineDrawer, CandleChartDrawer
from lib.factories import VertexesFactory
from lib.models import Line, Candle


class ChartController:

    def __init__(self):
        self._app = QtWidgets.QApplication(sys.argv)

        self._chartRepository = ChartRepository()

        thread_chart_drawer = threading.Thread(target=self._runChart, args=())
        thread_chart_drawer.start()

        self._view = MainView()

        self.states = {
            "drawers": {
                "grid" : GridDrawer, 
                "vertex" : LineChartDrawer,
                "maxMin" : MaxMinValuesDrawer,
                "line" : LineDrawer
            }
        } 

        self._init()


    def _init(self):
        self._view.chart.candleChartTypeButton.clicked.connect(
            self.changeVertexesTypeCandle)
        self._view.chart.lineChartTypeButton.clicked.connect(
            self.changeVertexesTypeLine)
        for i in self._view.chart.timestampFrame.children():
            if isinstance(i, QtWidgets.QPushButton):
                i.clicked.connect(self.changeTypeStamp)

    # def _move

    def changeVertexesTypeCandle(self):
        VertexesFactory.Type = Candle
        self.states["drawers"]["vertex"] = CandleChartDrawer
        self._view.updateCanvas()

    def changeVertexesTypeLine(self):
        VertexesFactory.Type = Line
        self.states["drawers"]["vertex"] = LineChartDrawer
        self._view.updateCanvas()

    def changeTypeStamp(self):
        sender = self._view.sender()
        Connection.updateTimeStamp(sender.text())

    def _runChart(self):

        data = self._getChartData()
        data.reverse()

        self._view.setCanvasStates(self.states)
        self._view.setCanvasData(data)
        self._view.updateCanvas()

        time.sleep(0.1)
        self._runChart()

    def _getChartData(self):
        return json.loads(self._chartRepository.getRemoteData())

    def run(self):
        self._view.show()
        return self._app.exec_()
