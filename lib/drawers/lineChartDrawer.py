from PyQt5.QtGui import QColor, QPen
from . import Drawer
from ..positioners import ChartPositioner, Limiter
from ..factories import VertexesFactory 

class LineChartDrawer(Drawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)

    def draw(self, data):
        for i in range(0,  len(Limiter.drawableData)):
            pen = QPen(QColor("#00D3FF"), 3)
            self.painter.setPen(pen)

            if (i == 0):
                self.painter.drawLine(
                    self.width - ChartPositioner.paddingHorizontal -
                    (i) * VertexesFactory.Type.width,
                    self.getVerticalPosition(data[i].closePrice),
                    self.width - ChartPositioner.paddingHorizontal -
                    (i + 1) * VertexesFactory.Type.width,
                    self.getVerticalPosition(data[i].openPrice),
                )
                continue

            self.painter.drawLine(
                self.width - ChartPositioner.paddingHorizontal - i * VertexesFactory.Type.width,
                self.getVerticalPosition(data[i - 1].openPrice),
                self.width - ChartPositioner.paddingHorizontal -
                (i + 1) * VertexesFactory.Type.width,
                self.getVerticalPosition(data[i].openPrice),
            )