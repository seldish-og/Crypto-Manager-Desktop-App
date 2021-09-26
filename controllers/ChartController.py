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

        self._view = MainView()

        # иницилизация пиксмапа
        self._view.createPainter()

        self._states = {
            "loader": Loader(self._view.painter),
            "connectionChart": self.getChartData,
            "gridDrawer": GridDrawer(self._view.painter).draw,
            "vertexDrawer": LineChartDrawer(self._view.painter),
        }

        # поток отрисовки графика
        thread_chart_drawer = threading.Thread(target=self.runChart, args=())
        thread_chart_drawer.start()

        # логика отрисовки
        self._view.closePainter()

        # установка пиксмапа
        self._view.setPainter()

    def runChart(self):

        self.data = None

        self._view.clearPainter()

        for state in self._states.keys():

            action = self._states[state]

            if state == "loader":
                pass

            if state == "connectionChart":
                self.data = action()

            if state == "gridDrawer":
                if not self.data:
                    print("data is None")
                    return

                action(self.data)

            if state == "vertexDrawer":
                pass

    def getChartData(self):
        data = self._chartRepository.getRemoteData()
        return self._vertexesFactory.createVertexes(json.loads(data))

    def run(self):
        self._view.show()
        return self._app.exec_()
