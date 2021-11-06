from ..models import Line


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
