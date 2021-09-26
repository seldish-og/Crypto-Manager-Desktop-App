from controllers.ChartController import ChartController
import sys

from PyQt5.QtWidgets import QApplication
from views.MainView import MainView
from controllers.ChartController import ChartController

if __name__ == '__main__':
    controller = ChartController()
    sys.exit(controller.run())

