import math
from decimal import Decimal

from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from . import Drawer
from ..themes import ThemeHolder


class NiceScale:
    def __init__(self, minv, maxv):
        self.maxTicks = 6
        self.tickSpacing = 0
        self.lst = 10
        self.niceMin = 0
        self.niceMax = 0
        self.minPoint = minv
        self.maxPoint = maxv
        self.calculate()

    def calculate(self):
        self.lst = self.niceNum(
            Decimal(str(self.maxPoint)) - Decimal(str(self.minPoint)), False)
        self.tickSpacing = self.niceNum(
            Decimal(str(self.lst)) / (Decimal(str(self.maxTicks)) - Decimal(str(1))), True)
        self.niceMin = math.floor(Decimal(str(
            self.minPoint)) / Decimal(str(self.tickSpacing))) * Decimal(str(self.tickSpacing))
        self.niceMax = math.ceil(Decimal(str(
            self.maxPoint)) / Decimal(str(self.tickSpacing))) * Decimal(str(self.tickSpacing))

    def niceNum(self, lst, rround):
        self.lst = lst
        exponent = 0  # exponent of range */
        fraction = 0  # fractional part of range */
        niceFraction = 0  # nice, rounded fraction */

        exponent = math.floor(math.log10(self.lst))
        fraction = Decimal(str(self.lst)) / \
            Decimal(str(math.pow(10, exponent)))

        if (self.lst):
            if (fraction < 1.5):
                niceFraction = 1
            elif (fraction < 3):
                niceFraction = 2
            elif (fraction < 7):
                niceFraction = 5
            else:
                niceFraction = 10
        else:
            if (fraction <= 1):
                niceFraction = 1
            elif (fraction <= 2):
                niceFraction = 2
            elif (fraction <= 5):
                niceFraction = 5
            else:
                niceFraction = 10

        return Decimal(str(niceFraction)) * Decimal(str(math.pow(10, exponent)))

    def setMinMaxPoints(self, minPoint, maxPoint):
        self.minPoint = minPoint
        self.maxPoint = maxPoint
        self.calculate()

    def setMaxTicks(self, maxTicks):
        self.maxTicks = maxTicks
        self.calculate()


class GridDrawer(Drawer):
    def __init__(self, painter: QPainter) -> None:
        super().__init__(painter)

    def draw(self, data):
        gridSettings = NiceScale(Drawer.minimalValue, Drawer.maximalValue)
        # print("a.lst ", gridSettings.lst)
        # print("a.maxPoint ", gridSettings.maxPoint)
        # print("a.maxTicks ", gridSettings.maxTicks)
        # print("a.minPoint ", gridSettings.minPoint)
        # print("a.niceMax ", gridSettings.niceMax)
        # print("a.niceMin ", gridSettings.niceMin)
        # print("a.tickSpacing ", gridSettings.tickSpacing)

        maximalLength = len(str(Decimal(Drawer.maximalValue) % 1)[:2])

        grid = []
        for i in range(gridSettings.maxTicks * -2, gridSettings.maxTicks * 2):
            grid.append(float(Decimal(str(gridSettings.niceMin)) +
                        Decimal(str(i)) * Decimal(str(gridSettings.tickSpacing))))

        for i in grid:
            if (len(str(Decimal(str(i)) % 1)) - 2 > maximalLength):
                maximalLength = len(str(Decimal(str(i)) % 1)) - 2


        for i in grid:
            pen = QPen(QColor(ThemeHolder.theme.gridLineColor), 1)
            self.painter.setPen(pen)
            self.painter.drawLine(
                0,
                self.getVerticalPosition(i),
                self.width,
                self.getVerticalPosition(i),
            )
            text = str(("{0:." + str(maximalLength) + "f}").format(i))
            font = QFont("times", 8)
            fm = QFontMetrics(font)
            pen = QPen(QColor(ThemeHolder.theme.textColor), 2)
            self.painter.setPen(pen)
            self.painter.setFont(font)
            self.painter.drawText(self.width - fm.width(text),
                                  (self.getVerticalPosition(i) - fm.height() / 2), text)
