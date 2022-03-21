# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chart.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(866, 600)
        MainWindow.setStyleSheet(u"background-color: #111E2E;\n"
"border: none;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(53, 0))
        self.frame.setMaximumSize(QSize(60, 16777215))
        self.frame.setStyleSheet(u"color: #fff;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.currencyFrame = QFrame(self.frame)
        self.currencyFrame.setObjectName(u"currencyFrame")
        self.currencyFrame.setFrameShape(QFrame.StyledPanel)
        self.currencyFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.currencyFrame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.logo = QLabel(self.currencyFrame)
        self.logo.setObjectName(u"logo")
        self.logo.setStyleSheet(u"margin-bottom: 4px;\n"
"margin-top: 6px;")
        self.logo.setPixmap(QPixmap(u":/images/logo.png"))

        self.verticalLayout_2.addWidget(self.logo, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.symbol = QPushButton(self.currencyFrame)
        self.symbol.setObjectName(u"symbol")
        self.symbol.setStyleSheet(u"margin-bottom: 35px;")

        self.verticalLayout_2.addWidget(self.symbol)


        self.verticalLayout.addWidget(self.currencyFrame, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.timestampFrame = QFrame(self.frame)
        self.timestampFrame.setObjectName(u"timestampFrame")
        self.timestampFrame.setStyleSheet(u"QPushButton {\n"
"	border-top: 1px solid #00D3FF;\n"
"	padding: 16px 0;\n"
"	font-size: 19px;\n"
"}\n"
"\n"
"QPushButton:focus {\n"
"	background-color: rgba(0, 211, 255, .21);\n"
"}\n"
"")
        self.timestampFrame.setFrameShape(QFrame.StyledPanel)
        self.timestampFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.timestampFrame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.dayThreeTimestampButton = QPushButton(self.timestampFrame)
        self.dayThreeTimestampButton.setObjectName(u"dayThreeTimestampButton")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dayThreeTimestampButton.sizePolicy().hasHeightForWidth())
        self.dayThreeTimestampButton.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.dayThreeTimestampButton)

        self.dayTimestampButton = QPushButton(self.timestampFrame)
        self.dayTimestampButton.setObjectName(u"dayTimestampButton")

        self.verticalLayout_3.addWidget(self.dayTimestampButton)

        self.fourHourTimestampButton = QPushButton(self.timestampFrame)
        self.fourHourTimestampButton.setObjectName(u"fourHourTimestampButton")

        self.verticalLayout_3.addWidget(self.fourHourTimestampButton)

        self.hourTimestampButton = QPushButton(self.timestampFrame)
        self.hourTimestampButton.setObjectName(u"hourTimestampButton")

        self.verticalLayout_3.addWidget(self.hourTimestampButton)

        self.minuteTimestampButton = QPushButton(self.timestampFrame)
        self.minuteTimestampButton.setObjectName(u"minuteTimestampButton")
        self.minuteTimestampButton.setStyleSheet(u"border-bottom: 1px solid #00D3FF;\n"
"margin-bottom: 53px;")

        self.verticalLayout_3.addWidget(self.minuteTimestampButton)


        self.verticalLayout.addWidget(self.timestampFrame, 0, Qt.AlignTop)

        self.chatTypeFrame = QFrame(self.frame)
        self.chatTypeFrame.setObjectName(u"chatTypeFrame")
        self.chatTypeFrame.setStyleSheet(u"margin-bottom: 18px;")
        self.chatTypeFrame.setFrameShape(QFrame.StyledPanel)
        self.chatTypeFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.chatTypeFrame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.candleChartTypeButton = QPushButton(self.chatTypeFrame)
        self.candleChartTypeButton.setObjectName(u"candleChartTypeButton")
        icon = QIcon()
        icon.addFile(u":/images/candle_type.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.candleChartTypeButton.setIcon(icon)
        self.candleChartTypeButton.setIconSize(QSize(40, 40))

        self.verticalLayout_4.addWidget(self.candleChartTypeButton)

        self.lineChartTypeButton = QPushButton(self.chatTypeFrame)
        self.lineChartTypeButton.setObjectName(u"lineChartTypeButton")
        icon1 = QIcon()
        icon1.addFile(u":/images/line_type.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.lineChartTypeButton.setIcon(icon1)
        self.lineChartTypeButton.setIconSize(QSize(40, 40))

        self.verticalLayout_4.addWidget(self.lineChartTypeButton, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout.addWidget(self.chatTypeFrame, 0, Qt.AlignTop)


        self.horizontalLayout.addWidget(self.frame, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.lineFrame = QFrame(self.centralwidget)
        self.lineFrame.setObjectName(u"lineFrame")
        self.lineFrame.setFrameShape(QFrame.StyledPanel)
        self.lineFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.lineFrame)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.sidebarLine = QFrame(self.lineFrame)
        self.sidebarLine.setObjectName(u"sidebarLine")
        self.sidebarLine.setStyleSheet(u"border-left: 1px solid #00D3FF;")
        self.sidebarLine.setFrameShape(QFrame.VLine)
        self.sidebarLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.sidebarLine)


        self.horizontalLayout.addWidget(self.lineFrame, 0, Qt.AlignLeft)

        self.symbols = QFrame(self.centralwidget)
        self.symbols.setObjectName(u"symbols")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.symbols.sizePolicy().hasHeightForWidth())
        self.symbols.setSizePolicy(sizePolicy1)
        self.symbols.setMinimumSize(QSize(200, 0))
        self.symbols.setFrameShape(QFrame.StyledPanel)
        self.symbols.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.symbols)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.symbolInput = QLineEdit(self.symbols)
        self.symbolInput.setObjectName(u"symbolInput")
        self.symbolInput.setStyleSheet(u"border-bottom: 2px solid white;\n"
"color: white;\n"
"padding-bottom: 2px;\n"
"font-size: 14px;")

        self.verticalLayout_6.addWidget(self.symbolInput)

        self.scrollArea = QScrollArea(self.symbols)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 182, 553))
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy2)
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.appendHere = QFrame(self.scrollAreaWidgetContents)
        self.appendHere.setObjectName(u"appendHere")
        self.appendHere.setFrameShape(QFrame.StyledPanel)
        self.appendHere.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.appendHere)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_7.addWidget(self.appendHere, 0, Qt.AlignTop)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_6.addWidget(self.scrollArea)


        self.horizontalLayout.addWidget(self.symbols)

        self.chartFrame = QFrame(self.centralwidget)
        self.chartFrame.setObjectName(u"chartFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.chartFrame.sizePolicy().hasHeightForWidth())
        self.chartFrame.setSizePolicy(sizePolicy3)
        self.chartFrame.setFrameShape(QFrame.StyledPanel)
        self.chartFrame.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.chartFrame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.logo.setText("")
        self.symbol.setText(QCoreApplication.translate("MainWindow", u"BTCUSDT", None))
        self.dayThreeTimestampButton.setText(QCoreApplication.translate("MainWindow", u"3d", None))
        self.dayTimestampButton.setText(QCoreApplication.translate("MainWindow", u"1d", None))
        self.fourHourTimestampButton.setText(QCoreApplication.translate("MainWindow", u"4h", None))
        self.hourTimestampButton.setText(QCoreApplication.translate("MainWindow", u"1h", None))
        self.minuteTimestampButton.setText(QCoreApplication.translate("MainWindow", u"1m", None))
        self.candleChartTypeButton.setText("")
        self.lineChartTypeButton.setText("")
        self.symbolInput.setText(QCoreApplication.translate("MainWindow", u"BTCUSDT", None))
    # retranslateUi

