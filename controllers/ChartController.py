import json
import sys
import asyncio
import threading

from models.Candle import Candle
from models.Line import Line
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPen, QPixmap
from views.MainView import GridDrawer, LineChartDrawer, Loader, MainView

from repository.ChartRepository import ChartRepository
import time


class VertexesFactory:

    def __init__(self) -> None:
        self.newVertexes = []

    def createVertex(self, vertex, type=Candle):
        return type(vertex)

    def createVertexes(self, vertexes, type=Candle):
        for i in vertexes:
            self.newVertexes.append(type(i))
        return self.newVertexes


class ChartController:

    def __init__(self):
        self._app = QtWidgets.QApplication(sys.argv)

        self._chartRepository = ChartRepository()
        self._vertexesFactory = VertexesFactory()

        thread_chart_drawer = threading.Thread(target=self._runChart, args=())
        thread_chart_drawer.start()

        self._view = MainView()


    def _runChart(self):
        data = self._getChartData()
        data.reverse()

        self._view.setCanvasData(data)
        self._view.updateCanvas()

    def _getChartData(self):
        data = self._chartRepository.getRemoteData()
        return self._vertexesFactory.createVertexes(json.loads(data))

    def run(self):
        self._view.show()
        return self._app.exec_()
