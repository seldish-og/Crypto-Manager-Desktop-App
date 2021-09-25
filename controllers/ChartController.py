import json
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
        self.chartRepository = ChartRepository()
        self.vertexesFactory = VertexesFactory()

    def getChartData(self):
        data = self.chartRepository.getRemoteData()
        return self.vertexesFactory.createVertexes(json.loads(data))

