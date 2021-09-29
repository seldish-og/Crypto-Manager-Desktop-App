import json
from repository.Connection import Connection
import sys
import asyncio
import threading

from models.Candle import Candle
from models.Line import Line
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPen, QPixmap
from views.MainView import CandleChartDrawer, GridDrawer, LineChartDrawer, Loader, MainView

from repository.ChartRepository import ChartRepository
import time


class VertexesFactory:
    Type = Line

    def __init__(self) -> None:
        self.newVertexes = []

    def createVertex(self, vertex):
        return type(vertex)

    def createVertexes(self, vertexes):
        for i in vertexes:
            self.newVertexes.append(VertexesFactory.Type(i))
        return self.newVertexes


class ChartController:

    def __init__(self):
        self._app = QtWidgets.QApplication(sys.argv)

        self._chartRepository = ChartRepository()
        self._vertexesFactory = VertexesFactory()

        thread_chart_drawer = threading.Thread(target=self._runChart, args=())
        thread_chart_drawer.start()

        self._view = MainView()

        self.states = {
            "gridDrawer": GridDrawer,
            "vertexDrawer": LineChartDrawer,
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

        time.sleep(1)
        self._runChart()


    def _getChartData(self):
        data = self._chartRepository.getRemoteData()
        return self._vertexesFactory.createVertexes(json.loads(data))

    def run(self):
        self._view.show()
        return self._app.exec_()
