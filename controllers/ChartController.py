import json
from repository.Connection import Connection
import sys
import asyncio
import threading

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPen, QPixmap
from views.MainView import MainView

from repository.ChartRepository import ChartRepository
import time

from Chartilo import GridDrawer, LineChartDrawer, VertexesFactory, Candle, Line, CandleChartDrawer


class Ass:
    def __init__(self) -> None:
        pass


class ChartController:

    def __init__(self):
        self._app = QtWidgets.QApplication(sys.argv)

        self._chartRepository = ChartRepository()

        thread_chart_drawer = threading.Thread(target=self._runChart, args=())
        thread_chart_drawer.start()

        self._view = MainView()

        self.states = {
            "drawers": [GridDrawer, LineChartDrawer]
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

    def changeVertexesTypeCandle(self):
        VertexesFactory.Type = Candle
        self.states["vertexDrawer"] = CandleChartDrawer

    def changeVertexesTypeLine(self):
        VertexesFactory.Type = Line
        self.states["vertexDrawer"] = LineChartDrawer

    def changeTypeStamp(self):
        sender = self._view.sender()
        Connection.updateTimeStamp(sender.text())

    def _runChart(self):

        data = self._getChartData()
        data.reverse()

        self._view.setCanvasStates(self.states)
        self._view.setCanvasData(data)
        self._view.updateCanvas()

        self._runChart()

    def _getChartData(self):
        return json.loads(self._chartRepository.getRemoteData())

    def run(self):
        self._view.show()
        return self._app.exec_()
