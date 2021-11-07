from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPen
from . import Drawer
from ..themes import ThemeHolder


class MaxMinValuesDrawer(Drawer):
    def __init__(self, painter) -> None:
        super().__init__(painter)

    def draw(self, data):
        # maximal point
        pen = QPen(QColor(ThemeHolder.theme.bullColor), 0.5)
        self.painter.setPen(pen)
        self.painter.drawLine(
            0,
            self.getVerticalPosition(Drawer.maximalValue),
            self.width,
            self.getVerticalPosition(Drawer.maximalValue),
        )
        text = str(self.maximalValue)
        font = QFont("times", 10)
        fm = QFontMetrics(font)
        pen = QPen(QColor(ThemeHolder.theme.bullColor), 2)
        self.painter.setPen(pen)
        self.painter.setFont(font)
        self.painter.drawText(0, (self.getVerticalPosition(
            Drawer.maximalValue) - fm.height() / 2), text)

        # minimal point
        pen = QPen(QColor(ThemeHolder.theme.bearColor), 0.5)
        self.painter.setPen(pen)
        self.painter.drawLine(
            0,
            self.getVerticalPosition(Drawer.minimalValue),
            self.width,
            self.getVerticalPosition(Drawer.minimalValue),
        )
        text = str(self.minimalValue)
        font = QFont("times", 10)
        fm = QFontMetrics(font)
        pen = QPen(QColor(ThemeHolder.theme.bearColor), 2)
        self.painter.setPen(pen)
        self.painter.setFont(font)
        self.painter.drawText(0, (self.getVerticalPosition(
            self.minimalValue) - fm.height() / 2), text)


