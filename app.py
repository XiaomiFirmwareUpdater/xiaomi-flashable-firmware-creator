#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""Xiaomi Flashable Firmware Creator GUI"""

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, qApp
from PyQt5.QtGui import QIcon


class MainWindowUi(QMainWindow):
    """Main Window"""
    def __init__(self):
        super(MainWindowUi, self).__init__()
        self.window_body = QtWidgets.QWidget(self)
        self.process_type = QtWidgets.QGroupBox(self.window_body)
        self.btn_fw = QtWidgets.QRadioButton(self.process_type)
        self.btn_nonarb = QtWidgets.QRadioButton(self.process_type)
        self.btn_vendor = QtWidgets.QRadioButton(self.process_type)
        self.btn_fwless = QtWidgets.QRadioButton(self.process_type)
        self.groupbox_drop = QtWidgets.QGroupBox(self.window_body)
        self.label_drop = QtWidgets.QLabel(self.groupbox_drop)
        self.frame = QtWidgets.QFrame(self.window_body)
        self.btn_select = QtWidgets.QPushButton(self.frame)
        self.btn_create = QtWidgets.QPushButton(self.frame)
        self.status_box = QtWidgets.QGroupBox(self.window_body)
        self.menubar = QtWidgets.QMenuBar(self)
        self.label = QtWidgets.QLabel(self.status_box)
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.action_open_zip = QtWidgets.QAction(self)
        self.action_quit = QtWidgets.QAction(self)
        self.action_help = QtWidgets.QAction(self)
        self.action_donate = QtWidgets.QAction(self)
        self.action_about = QtWidgets.QAction(self)
        self.action_report_bug = QtWidgets.QAction(self)
        self.setup_ui(self)
        self.setWindowIcon(QIcon('icon.png'))
        self.setAcceptDrops(True)
        self.center()
        self.show()

    def setup_ui(self, main_window):
        """
        setup window ui
        """
        # Main Window
        main_window.setObjectName("main_window")
        main_window.setEnabled(True)
        main_window.resize(600, 400)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                            QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(size_policy)
        main_window.setMinimumSize(QtCore.QSize(600, 0))
        main_window.setMaximumSize(QtCore.QSize(600, 400))
        self.window_body.setObjectName("window_body")
        main_window.setCentralWidget(self.window_body)
        # GroupBox: process_type
        self.process_choose()
        # GroupBox: Drop files
        self.file_dropper()
        # Frame: Status
        self.status_frame()
        # Menubar
        self.menu_bar(main_window)
        # UI Strings
        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def process_choose(self):
        """
        GroupBox: process_type
        """
        self.process_type.setGeometry(QtCore.QRect(10, 40, 161, 141))
        self.process_type.setObjectName("process_type")
        self.btn_fw.setGeometry(QtCore.QRect(0, 20, 109, 30))
        self.btn_fw.setObjectName("btn_fw")
        self.btn_nonarb.setGeometry(QtCore.QRect(0, 50, 161, 30))
        self.btn_nonarb.setObjectName("btn_nonarb")
        self.btn_vendor.setGeometry(QtCore.QRect(0, 80, 161, 30))
        self.btn_vendor.setObjectName("btn_vendor")
        self.btn_fwless.setGeometry(QtCore.QRect(0, 110, 161, 30))
        self.btn_fwless.setObjectName("btn_fwless")

    def file_dropper(self):
        """
        GroupBox: Drop files
        """
        self.groupbox_drop.setGeometry(QtCore.QRect(190, 40, 391, 141))
        self.groupbox_drop.setObjectName("groupbox_drop")
        self.groupbox_drop.setAcceptDrops(True)
        self.label_drop.setGeometry(QtCore.QRect(0, 30, 381, 111))
        self.label_drop.setFrameShape(QtWidgets.QFrame.Box)
        self.label_drop.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_drop.setLineWidth(2)
        self.label_drop.setAlignment(QtCore.Qt.AlignCenter)
        self.label_drop.setObjectName("label_drop")

    def status_frame(self):
        """
        Frame: Status
        """
        self.frame.setGeometry(QtCore.QRect(10, 190, 580, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.btn_select.setGeometry(QtCore.QRect(160, 20, 104, 37))
        self.btn_select.setObjectName("btn_select")
        self.btn_create.setGeometry(QtCore.QRect(280, 20, 104, 37))
        self.btn_create.setObjectName("btn_create")
        self.status_box.setGeometry(QtCore.QRect(10, 249, 580, 91))
        self.status_box.setObjectName("status_box")
        self.label.setGeometry(QtCore.QRect(0, 30, 581, 51))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setLineWidth(2)
        self.label.setText("")
        self.label.setObjectName("label")

    def menu_bar(self, main_window):
        """
        Menubar
        """
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 32))
        self.menubar.setObjectName("menubar")
        self.menu_file.setObjectName("menu_file")
        self.menu_help.setObjectName("menu_help")
        main_window.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.action_open_zip.setObjectName("action_open_zip")
        self.action_quit.setObjectName("action_quit")
        self.action_quit.setStatusTip("action_quit_tip")
        self.action_help.setObjectName("action_help")
        self.action_donate.setObjectName("action_donate")
        self.action_about.setObjectName("action_about")
        self.action_report_bug.setObjectName("action_report_bug")
        self.menu_file.addAction(self.action_open_zip)
        self.menu_file.addAction(self.action_quit)
        self.menu_help.addAction(self.action_help)
        self.menu_help.addAction(self.action_report_bug)
        self.menu_help.addAction(self.action_donate)
        self.menu_help.addAction(self.action_about)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        # Shortcuts
        self.action_open_zip.setShortcut('Ctrl+O')
        self.action_quit.setShortcut('Ctrl+Q')
        # Actions
        self.action_quit.triggered.connect(qApp.quit)

    def retranslate_ui(self, main_window):
        """
        Items strings
        """
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window",
                                              "Xiaomi Flashable Firmware Creator "
                                              "by XiaomiFirmwareUpdater"))
        self.process_type.setTitle(_translate("main_window", "Process"))
        self.btn_fw.setText(_translate("main_window", "Firmware"))
        self.btn_nonarb.setText(_translate("main_window", "Non-ARB Firmware"))
        self.btn_vendor.setText(_translate("main_window", "Firmware + Vendor"))
        self.btn_fwless.setText(_translate("main_window", "Firmware-less ROM"))
        self.groupbox_drop.setTitle(_translate("main_window", "Drop a file"))
        self.label_drop.setText(_translate("main_window",
                                           "<html><head/><body>"
                                           "<p align=\"center\">"
                                           "<span style=\" font-style:italic;\">"
                                           "Drop a rom zip file here"
                                           "</span></p></body></html>"))
        self.btn_select.setText(_translate("main_window", "Select file"))
        self.btn_create.setText(_translate("main_window", "Create"))
        self.status_box.setTitle(_translate("main_window", "Status"))
        self.menu_file.setTitle(_translate("main_window", "File"))
        self.menu_help.setTitle(_translate("main_window", "Help"))
        self.action_open_zip.setText(_translate("main_window", "Open ZIP"))
        self.action_quit.setText(_translate("main_window", "Quit"))
        self.action_quit.setStatusTip(_translate("action_quit_tip", "Exits the application"))
        self.action_help.setText(_translate("main_window", "What\'s This?"))
        self.action_donate.setText(_translate("main_window", "Donate"))
        self.action_about.setText(_translate("main_window", "About"))
        self.action_report_bug.setText(_translate("main_window", "Report Bug"))

    def center(self):
        """
        Dynamically center the window in screen
        """
        # https://gist.github.com/saleph/163d73e0933044d0e2c4
        # geometry of the main window
        window = self.frameGeometry()
        # center point of screen
        center_point = QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        window.moveCenter(center_point)
        # top left of rectangle becomes top left of window centering it
        self.move(window.topLeft())


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    WINDOW = MainWindowUi()
    sys.exit(APP.exec_())
