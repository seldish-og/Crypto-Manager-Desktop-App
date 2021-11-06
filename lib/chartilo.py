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
        painter = QPainter()
        painter.begin(self)

        if Chartilo.data == None or not Chartilo.data:
            print("There is no data to draw")
            return

        Limiter.setDrawableData(Limiter.calculateDrawableData(Chartilo.parsedData, 0, Limiter.getVertexesAmount(
            Chartilo.parsedData, VertexesFactory.Type.width, painter.device().width(), ChartPositioner.paddingHorizontal)))

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
                    painter).draw(Limiter.drawableData)
            except Exception as e:
                raise Exception(str(e) +
                                "\nThere is unexpected drawer: " + str(drawer))

        painter.end()

    def updateCanvas(self):
        Chartilo.parsedData = VertexesFactory().createVertexes(Chartilo.data)
        self.update()

    def setData(self, data):
        Chartilo.data = data

    def setStates(self, states):
        self.states = states
