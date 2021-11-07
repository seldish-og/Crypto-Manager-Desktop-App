from ..positioners import ChartPositioner


class Drawer:
    maximalValue = 0
    minimalValue = 0
    maxMinDifference = 0

    def __init__(self, painter) -> None:
        self.painter = painter
        self.height = painter.device().height()
        self.width = painter.device().width()

    @staticmethod
    def setMaxMinValue(data) -> None:
        minimum = float('inf')
        maximum = float('-inf')

        for vertex in data:

            vertex = vertex.__dict__

            for vertex_field in vertex.keys():
                if (vertex_field == "openTime"):
                    continue
                if float(vertex.get(vertex_field)) < minimum:
                    minimum = vertex.get(vertex_field)
                if float(vertex.get(vertex_field)) > maximum:
                    maximum = vertex.get(vertex_field)

        Drawer.maximalValue = maximum
        Drawer.minimalValue = minimum
        Drawer.maxMinDifference = maximum - minimum

    def getVerticalPosition(self, price) -> float:
        return self.height - ChartPositioner.paddingVertical - (Drawer.maxMinDifference - (Drawer.maximalValue - price)) / Drawer.maxMinDifference * (self.height - 2 * ChartPositioner.paddingVertical)
