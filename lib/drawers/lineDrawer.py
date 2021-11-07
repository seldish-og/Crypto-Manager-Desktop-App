from PyQt5 import QtCore
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QPen
from . import Drawer
from ..themes import ThemeHolder


class LineDrawer(Drawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)

    def draw(self, data):
        vertex = data[0]
        pen = QPen(QColor(ThemeHolder.theme.currentPriceLineColor), 1, QtCore.Qt.DashLine)
        self.painter.setPen(pen)
        self.painter.drawLine(
            0,
            self.getVerticalPosition(vertex.closePrice),
            self.width,
            self.getVerticalPosition(vertex.closePrice),
        )
        text = str(vertex.closePrice)
        font = QFont("times", 12)
        fm = QFontMetrics(font)
        self.painter.setBrush(QBrush(QColor(ThemeHolder.theme.chartLineColor)))
        self.painter.drawRect(
            self.width - fm.width(text) - 5,
            self.getVerticalPosition(vertex.closePrice) - fm.height() / 2 - 2,
            fm.width(text) + 5,
            fm.height() + 1,
        )
        pen = QPen(QColor(ThemeHolder.theme.textColor), 3)
        self.painter.setPen(pen)
        self.painter.setFont(font)
        self.painter.drawText(self.width - fm.width(text),
                              (self.getVerticalPosition(vertex.closePrice) + fm.height() / 4), text)