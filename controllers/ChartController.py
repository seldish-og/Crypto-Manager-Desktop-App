import re
import sys
import json
import threading
import time
from tkinter import W

from PyQt5 import QtCore, QtWidgets
from views.MainView import MainView

from repository.Connection import Connection
from PyQt5.QtGui import QPainter, QPen, QPixmap
from repository.ChartRepository import ChartRepository

from chartilo.drawers import GridDrawer, LineChartDrawer, MaxMinValuesDrawer, LineDrawer, CandleChartDrawer
from chartilo.factories import VertexesFactory
from chartilo.models import Line, Candle

from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QFrame

class ChartController:

    def __init__(self):
        self._app = QtWidgets.QApplication(sys.argv)

        self._chartRepository = ChartRepository()

        self.symbols = []

        thread_chart_drawer = threading.Thread(target=self._runChart, args=())
        thread_chart_drawer.start()

        self._view = MainView(self)

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

    def changeCurrencySymbol(self, obj, event):
        if isinstance(obj, QFrame) and event.type() == QtCore.QEvent.MouseButtonPress:
            Connection.PREVIOUS_CHART_URL = Connection.FETCH_CHART_URL
            Connection.FETCH_CHART_URL = re.sub(r"symbol=[A-Z]+", "symbol=" + obj.objectName(), Connection.FETCH_CHART_URL)
            self._view.chart.symbol.setText(obj.objectName())
            self._view.chart.symbolInput.setText(obj.objectName())

    def openSymbolsList(self):
        if self.isSymbolVisible == True:
            self._view.chart.symbols.setVisible(False)
            self.isSymbolVisible = False
        else:
            self._view.chart.symbols.setVisible(True)
            self.isSymbolVisible = True

    def _init(self):
        self.isSymbolVisible = True


        self._view.chart.symbol.clicked.connect(self.openSymbolsList)
        self._view.chart.symbolInput.textEdited.connect(self.searchSymbols)
        self._view.chart.lineChartTypeButton.clicked.connect(self.changeVertexesTypeLine)
        self._view.chart.candleChartTypeButton.clicked.connect(self.changeVertexesTypeCandle)

        for i in self._view.chart.timestampFrame.children():
            if isinstance(i, QtWidgets.QPushButton):
                i.clicked.connect(self.changeTypeStamp)

        self.openSymbolsList()
        self.symbols = [symbol["symbol"] for symbol in self._getSymbols()]
        self._view.appendSymbols(self.symbols)

    def searchSymbols(self):
        symbol = self._view.chart.symbolInput.text().upper()

        if len(symbol) < 3:
            return

        array = []

        for symbols_item in self.symbols:
            if (symbols_item.startswith(symbol)):
                array.append(symbols_item)

        self._view.appendSymbols(sorted(array))

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

    def _getSymbols(self):
        return json.loads(self._chartRepository.getRemoteSymbols())

    def run(self):
        self._view.show()
        return self._app.exec_()
