from sys import setprofile
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from .drawers import Drawer
from .positioners import Limiter, ChartPositioner
from .models import Line, Candle
from .factories import VertexesFactory
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget


class Chartilo(QWidget):
    data = None

    def __init__(self) -> None:
        super(Chartilo, self).__init__()

    def paintEvent(self, event) -> None:
        self.painter = QPainter()
        self.painter.begin(self)

        if Chartilo.data == None or not Chartilo.data:
            print("There is no data to draw")
            return

        vertexesAmount = Limiter.getVertexesAmount(Chartilo.parsedData, VertexesFactory.Type.width, self.painter.device().width(), ChartPositioner.paddingHorizontal) + Limiter.vertexesOffset // VertexesFactory.Type.width
        Limiter.setDrawableData(Limiter.calculateDrawableData(Chartilo.parsedData, Limiter.vertexesOffset // VertexesFactory.Type.width, vertexesAmount))

        if (not Limiter.drawableData):
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
            raise Exception(e + "\nThere is not enough state: drawers")

        for drawer in self.states["drawers"]:
            try:
                self.states["drawers"][drawer](
                    self.painter).draw(Limiter.drawableData)
            except Exception as e:
                raise Exception(str(e) +
                                "\nThere is unexpected drawer: " + str(drawer))

        self.painter.end()

    def updateCanvas(self):
        Chartilo.parsedData = VertexesFactory().createVertexes(Chartilo.data)
        self.update()

    def setData(self, data):
        Chartilo.data = data

    def setStates(self, states):
        self.states = states

    def mousePressEvent(self, event):
        print("Pressed")
        self.beginPosition = int(event.x())
        self.previousMove = self.beginPosition

    def mouseMoveEvent(self, event):
        motion = int(event.x())

        print(Limiter.vertexesOffset // VertexesFactory.Type.width, len(Chartilo.data), )

        speed = int(2 * VertexesFactory.Type.width)

        if (motion > self.previousMove):
            if (not ChartPositioner.paddingHorizontal < 0 and Limiter.vertexesOffset == 0):
                ChartPositioner.paddingHorizontal -= speed
            else:
                if (not len(Chartilo.data) < (Limiter.vertexesOffset + speed) // VertexesFactory.Type.width + Limiter.getVertexesAmount(Chartilo.parsedData, VertexesFactory.Type.width, self.painter.device().width(), ChartPositioner.paddingHorizontal)):
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
        print("Released")
        self.endPosition = event.x()
