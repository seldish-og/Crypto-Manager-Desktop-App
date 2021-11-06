from . import Drawer
from ..positioners import Limiter, ChartPositioner
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen


class CandleChartDrawer(Drawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)

    def draw(self, data):
        for i in range(0, len(Limiter.drawableData)):

            pen = QPen(QColor("#26a69a"), data[i].width - 3)

            if (data[i].openPrice > data[i].closePrice):
                pen = QPen(QColor("#ef5350"), data[i].width - 3)

            self.painter.setPen(pen)

            self.painter.drawLine(
                self.width - ChartPositioner.paddingHorizontal -
                i * data[i].width,
                self.getVerticalPosition(data[i].openPrice),
                self.width - ChartPositioner.paddingHorizontal -
                (i) * data[i].width,
                self.getVerticalPosition(data[i].closePrice),
            )

            pen.setWidth(1)
            self.painter.setPen(pen)

            self.painter.drawLine(
                self.width - ChartPositioner.paddingHorizontal -
                i * data[i].width,
                self.getVerticalPosition(data[i].minimalPrice),
                self.width - ChartPositioner.paddingHorizontal -
                i * data[i].width,
                self.getVerticalPosition(data[i].maximalPrice),
            )
