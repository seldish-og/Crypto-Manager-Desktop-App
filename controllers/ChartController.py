import json
import sys

from PyQt5 import QtWidgets

from views.MainView import MainView, Loader, GridDrawer, LineChartDrawer

from repository.ChartRepository import ChartRepository
from models.Candle import Candle
from models.Line import Line


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

        # self._states = {
        #     "loader": Loader(self._view.painter),
        #     "connectionChart": ChartController().getChartData,
        #     "gridDrawer": GridDrawer(self._view.painter),
        #     "vertexDrawer": LineChartDrawer(self._view.painter),
        # }

    def getChartData(self):
        data = self.chartRepository.getRemoteData()
        return self.vertexesFactory.createVertexes(json.loads(data))

    def run(self):
        self._view.show()
        return self._app.exec_()

