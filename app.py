import sys

from PyQt5.QtWidgets import QApplication
from views.MainView import MainView

if __name__ == '__main__':
    print("Hello there")
    app = QApplication(sys.argv)
    ex = MainView()
    ex.show()
    sys.exit(app.exec())

