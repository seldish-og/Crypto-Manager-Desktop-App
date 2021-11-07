from sys import setprofile
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from .drawers import Drawer
from .positioners import Limiter, ChartPositioner
from .models import Line, Candle
from .factories import VertexesFactory
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtWidgets import QWidget
from .themes import ThemeHolder


class Chartilo(QWidget):
    data = None
    parsedData = None

    def __init__(self) -> None:
        super(Chartilo, self).__init__()

    def resizeEvent(self, event):
        try:
            amountOnScreen = Limiter.getVertexesAmount(Chartilo.parsedData, VertexesFactory.Type.width, self.painter.device().width(), ChartPositioner.paddingHorizontal) + 1
            print(Limiter.vertexesOffset // VertexesFactory.Type.width + amountOnScreen, len(Chartilo.data), )
            if (Limiter.vertexesOffset // VertexesFactory.Type.width + amountOnScreen > len(Chartilo.data) ):
                Limiter.vertexesOffset -= ((Limiter.vertexesOffset // VertexesFactory.Type.width + amountOnScreen) - len(Chartilo.data)) * VertexesFactory.Type.width

        except Exception as e:
            pass

    def paintEvent(self, event) -> None:
        self.painter = QPainter()
        self.painter.begin(self)

        if not Chartilo.parsedData or not Chartilo.data:
            print("There is no data to draw")
            self.painter.end()
            return

        vertexesAmount = Limiter.getVertexesAmount(Chartilo.parsedData, VertexesFactory.Type.width, self.painter.device().width(), ChartPositioner.paddingHorizontal) + Limiter.vertexesOffset // VertexesFactory.Type.width
        Limiter.setDrawableData(Limiter.calculateDrawableData(Chartilo.parsedData, Limiter.vertexesOffset // VertexesFactory.Type.width, vertexesAmount))

        if (not Limiter.drawableData):
            print("There is no data to draw")
            return

        Drawer.setMaxMinValue(Limiter.drawableData)

        if (self.states.get("positions") is not None):
            for position in self.states["positions"]:
                if (position not in ChartPositioner.__dict__):
                    raise Exception("Unexpected field: " + position)
                setattr(ChartPositioner, position,
                        self.states["positions"][position])

        try:
            self.states["drawers"]
        except Exception as e:
            print(str(e) + "\nThere is not enough state: drawers")

        try:
            if (self.states.get("theme") is not None):
                ThemeHolder.theme = self.states["theme"]()
        except Exception as e:
            print("Тема не найдена")
            pass

        try:
            self.painter.setBrush(QBrush(QColor(ThemeHolder.theme.backgroundColor)))
            self.painter.drawRect(0, 0, self.painter.device().width(), self.painter.device().height())
        except Exception as e:
            print("Не удалось поменять фон, убедиться что в вашей теме он прописан")

        for drawer in self.states["drawers"]:
            try:
                self.states["drawers"][drawer](
                    self.painter).draw(Limiter.drawableData)
            except Exception as e:
                print(str(e) + "\nThere is unexpected drawer: " + str(drawer))

        self.painter.end()

    def updateCanvas(self):
        try:
            vertexType = self.states["type"]
            VertexesFactory.Type = vertexType
        except Exception as e:
            print(str(e))
            return
        Chartilo.parsedData = VertexesFactory().createVertexes(Chartilo.data)
        self.update()

    def setData(self, data):
        Chartilo.data = data

    def setStates(self, states):
        self.states = states

    def mousePressEvent(self, event):
        self.beginPosition = int(event.x())
        self.previousMove = self.beginPosition

    def mouseMoveEvent(self, event):
        motion = int(event.x())

        amountOnScreen = Limiter.getVertexesAmount(Chartilo.parsedData, VertexesFactory.Type.width, self.painter.device().width(), ChartPositioner.paddingHorizontal) + 1
        speed = int(2 * VertexesFactory.Type.width)

        if (motion > self.previousMove):
            if (not ChartPositioner.paddingHorizontal < 0 and Limiter.vertexesOffset == 0):
                ChartPositioner.paddingHorizontal -= speed
            else:
                if (not len(Chartilo.data) < (Limiter.vertexesOffset + speed) // VertexesFactory.Type.width + amountOnScreen):
                    Limiter.vertexesOffset += speed

        if (motion < self.previousMove):
            if (ChartPositioner.paddingHorizontal < ChartPositioner.maximalHorizontalPadding and Limiter.vertexesOffset == 0):
                ChartPositioner.paddingHorizontal += speed
            else:
                if (Limiter.vertexesOffset - speed < 0):
                    Limiter.vertexesOffset = 0
                else:
                    Limiter.vertexesOffset -= speed

        self.previousMove = motion
        self.updateCanvas()

    def mouseReleaseEvent(self, event):
        self.endPosition = event.x()
