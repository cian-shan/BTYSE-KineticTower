# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Idle_Leaderboard.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(643, 480)
        MainWindow.setStyleSheet("\n""background-color: rgb(154, 244, 244);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(30, 60, 571, 381))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 569, 379))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalSlider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.verticalSlider.setGeometry(QtCore.QRect(530, 20, 20, 341))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.textBrowser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 571, 381))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.raise_()
        self.verticalSlider.raise_()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, -10, 221, 61))
        self.label_3.setMaximumSize(QtCore.QSize(291, 91))
        font = QtGui.QFont()
        font.setFamily("Stencil")
        font.setPointSize(28)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("font: 48pt \"Stencil\";\n"
"font: 28pt \"Stencil\";")
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Leaderboard"))
