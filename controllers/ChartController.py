import re
import sys
import json
import threading
import time

from PyQt5 import QtCore, QtWidgets
from views.MainView import MainView

from repository.Connection import Connection
from PyQt5.QtGui import QPainter, QPen, QPixmap
from repository.ChartRepository import ChartRepository

from chartilo.drawers import GridDrawer, LineChartDrawer, MaxMinValuesDrawer, LineDrawer, CandleChartDrawer
from chartilo.factories import VertexesFactory
from chartilo.models import Line, Candle

from PyQt5.QtWidgets import QInputDialog


class ChartController:

    def __init__(self):
        self._app = QtWidgets.QApplication(sys.argv)

        self._chartRepository = ChartRepository()

        thread_chart_drawer = threading.Thread(target=self._runChart, args=())
        thread_chart_drawer.start()

        self._view = MainView()

        self.states = {
            "type": Line,
            "drawers": {
                "grid" : GridDrawer, 
                "vertex" : LineChartDrawer,
                "maxMin" : MaxMinValuesDrawer,
                "line" : LineDrawer
            }
        } 

        self._init()

    def changeCurrencySymbol(self):
        symbol, ok_pressed = QInputDialog.getText(self._view, "Input", "Enter symbos ex: btcusdt")
        if (ok_pressed):
            symbol = symbol.upper()
            Connection.PREVIOUS_CHART_URL = Connection.FETCH_CHART_URL
            Connection.FETCH_CHART_URL = re.sub(r"symbol=[A-Z]+", "symbol=" + symbol, Connection.FETCH_CHART_URL)


    def _init(self):
        self._view.chart.symbol.clicked.connect(self.changeCurrencySymbol)
        self._view.chart.candleChartTypeButton.clicked.connect(
            self.changeVertexesTypeCandle)
        self._view.chart.lineChartTypeButton.clicked.connect(
            self.changeVertexesTypeLine)
        for i in self._view.chart.timestampFrame.children():
            if isinstance(i, QtWidgets.QPushButton):
                i.clicked.connect(self.changeTypeStamp)

    # def _move

    def changeVertexesTypeCandle(self):
        self.states["type"] = Candle
        self.states["drawers"]["vertex"] = CandleChartDrawer
        self._view.updateCanvas()

    def changeVertexesTypeLine(self):
        self.states["type"] = Line
        self.states["drawers"]["vertex"] = LineChartDrawer
        self._view.updateCanvas()

    def changeTypeStamp(self):
        sender = self._view.sender()
        Connection.updateTimeStamp(sender.text())

    def _runChart(self):

        data = self._getChartData()
        # print(data)
        if (type(data) is dict):
            Connection.FETCH_CHART_URL = Connection.PREVIOUS_CHART_URL
            print(Connection.FETCH_CHART_URL, Connection.PREVIOUS_CHART_URL)
            self._runChart()

        self._view.chart.symbol.setText(re.search(r"symbol.(.*&)", Connection.FETCH_CHART_URL).group().replace("symbol=", "").replace("&", ""))
        data.reverse()

        self._view.setCanvasStates(self.states)
        self._view.setCanvasData(data)
        self._view.updateCanvas()

        time.sleep(0.1)
        self._runChart()

    def _getChartData(self):
        return json.loads(self._chartRepository.getRemoteData())

    def run(self):
        self._view.show()
        return self._app.exec_()
