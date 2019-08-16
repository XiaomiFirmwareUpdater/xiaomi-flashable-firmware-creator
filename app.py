# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(600, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(600, 0))
        MainWindow.setMaximumSize(QtCore.QSize(600, 400))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ProcessType = QtWidgets.QGroupBox(self.centralwidget)
        self.ProcessType.setGeometry(QtCore.QRect(10, 40, 161, 141))
        self.ProcessType.setObjectName("ProcessType")
        self.btn_fw = QtWidgets.QRadioButton(self.ProcessType)
        self.btn_fw.setGeometry(QtCore.QRect(0, 20, 109, 30))
        self.btn_fw.setObjectName("btn_fw")
        self.btn_nonarb = QtWidgets.QRadioButton(self.ProcessType)
        self.btn_nonarb.setGeometry(QtCore.QRect(0, 50, 161, 30))
        self.btn_nonarb.setObjectName("btn_nonarb")
        self.btn_vendor = QtWidgets.QRadioButton(self.ProcessType)
        self.btn_vendor.setGeometry(QtCore.QRect(0, 80, 161, 30))
        self.btn_vendor.setObjectName("btn_vendor")
        self.btn_fwless = QtWidgets.QRadioButton(self.ProcessType)
        self.btn_fwless.setGeometry(QtCore.QRect(0, 110, 161, 30))
        self.btn_fwless.setObjectName("btn_fwless")
        self.groupBox_drop = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_drop.setGeometry(QtCore.QRect(190, 40, 391, 141))
        self.groupBox_drop.setObjectName("groupBox_drop")
        self.label_drop = QtWidgets.QLabel(self.groupBox_drop)
        self.label_drop.setGeometry(QtCore.QRect(0, 30, 381, 111))
        self.label_drop.setStyleSheet("")
        self.label_drop.setFrameShape(QtWidgets.QFrame.Box)
        self.label_drop.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_drop.setLineWidth(2)
        self.label_drop.setAlignment(QtCore.Qt.AlignCenter)
        self.label_drop.setObjectName("label_drop")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 190, 580, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.btn_select = QtWidgets.QPushButton(self.frame)
        self.btn_select.setGeometry(QtCore.QRect(160, 20, 104, 37))
        self.btn_select.setObjectName("btn_select")
        self.btn_create = QtWidgets.QPushButton(self.frame)
        self.btn_create.setGeometry(QtCore.QRect(280, 20, 104, 37))
        self.btn_create.setObjectName("btn_create")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 249, 580, 91))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(0, 30, 581, 51))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setLineWidth(2)
        self.label.setText("")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 32))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_ZIP = QtWidgets.QAction(MainWindow)
        self.actionOpen_ZIP.setObjectName("actionOpen_ZIP")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionWhat_s_This = QtWidgets.QAction(MainWindow)
        self.actionWhat_s_This.setObjectName("actionWhat_s_This")
        self.actionDonate = QtWidgets.QAction(MainWindow)
        self.actionDonate.setObjectName("actionDonate")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionReport_Bug = QtWidgets.QAction(MainWindow)
        self.actionReport_Bug.setObjectName("actionReport_Bug")
        self.menuFile.addAction(self.actionOpen_ZIP)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionWhat_s_This)
        self.menuHelp.addAction(self.actionReport_Bug)
        self.menuHelp.addAction(self.actionDonate)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Xiaomi Flashable Firmware Creator by XiaomiFirmwareUpdater"))
        self.ProcessType.setTitle(_translate("MainWindow", "Process"))
        self.btn_fw.setText(_translate("MainWindow", "Firmware"))
        self.btn_nonarb.setText(_translate("MainWindow", "Non-ARB Firmware"))
        self.btn_vendor.setText(_translate("MainWindow", "Firmware + Vendor"))
        self.btn_fwless.setText(_translate("MainWindow", "Firmware-less ROM"))
        self.groupBox_drop.setTitle(_translate("MainWindow", "Drop a file"))
        self.label_drop.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-style:italic;\">Drop a rom zip file here</span></p></body></html>"))
        self.btn_select.setText(_translate("MainWindow", "Select file"))
        self.btn_create.setText(_translate("MainWindow", "Create"))
        self.groupBox.setTitle(_translate("MainWindow", "Status"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen_ZIP.setText(_translate("MainWindow", "Open ZIP"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionWhat_s_This.setText(_translate("MainWindow", "What\'s This?"))
        self.actionDonate.setText(_translate("MainWindow", "Donate"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionReport_Bug.setText(_translate("MainWindow", "Report Bug"))


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.center()
        self.show()

    def center(self):
        # https://gist.github.com/saleph/163d73e0933044d0e2c4
        # geometry of the main window
        qr = self.frameGeometry()
        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
