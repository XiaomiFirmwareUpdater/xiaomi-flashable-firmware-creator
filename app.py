#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""Xiaomi Flashable Firmware Creator GUI"""

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QMimeDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, qApp, QFileDialog, QGroupBox
from PyQt5.QtGui import QIcon
from helpers.settings import load_settings, update_settings
from helpers.language import load_strings, RTL_LANGUAGES


class DropSpace(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, file):
        file_type = QMimeDatabase().mimeTypeForFile(
            file.mimeData().urls()[0].toLocalFile()).name()
        if file_type == 'application/zip':
            file.accept()
        else:
            file.ignore()

    def dropEvent(self, file):
        filepath = file.mimeData().urls()[0].toLocalFile()
        WINDOW.filepath = filepath
        WINDOW.filename = filepath.split('/')[-1]
        WINDOW.status_label.setText(f"File {WINDOW.filename} is selected")


class MainWindowUi(QMainWindow):
    """Main Window"""
    def __init__(self):
        super(MainWindowUi, self).__init__()
        # Language related
        self.settings = load_settings()
        self.language = self.settings['language']
        self.translations = load_strings()
        self.strings = self.translations[self.language]
        # Init
        self.window_body = QtWidgets.QWidget(self)
        self.process_type = QtWidgets.QGroupBox(self.window_body)
        self.btn_fw = QtWidgets.QRadioButton(self.process_type)
        self.btn_nonarb = QtWidgets.QRadioButton(self.process_type)
        self.btn_vendor = QtWidgets.QRadioButton(self.process_type)
        self.btn_fwless = QtWidgets.QRadioButton(self.process_type)
        self.groupbox_drop = DropSpace(self.window_body)
        self.label_drop = QtWidgets.QLabel(self.groupbox_drop)
        self.frame = QtWidgets.QFrame(self.window_body)
        self.btn_select = QtWidgets.QPushButton(self.frame)
        self.btn_create = QtWidgets.QPushButton(self.frame)
        self.status_box = QtWidgets.QGroupBox(self.window_body)
        self.menubar = QtWidgets.QMenuBar(self)
        self.status_label = QtWidgets.QLabel(self.status_box)
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.menu_language = QtWidgets.QMenu(self.menubar)
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.action_open_zip = QtWidgets.QAction(self)
        self.action_quit = QtWidgets.QAction(self)
        self.action_language_en = QtWidgets.QAction(self)
        self.action_language_ar = QtWidgets.QAction(self)
        self.action_help = QtWidgets.QAction(self)
        self.action_donate = QtWidgets.QAction(self)
        self.action_about = QtWidgets.QAction(self)
        self.action_report_bug = QtWidgets.QAction(self)
        # vars
        self.filepath = ''
        self.filename = ''
        # setup
        self.setup_ui(self)
        self.setWindowIcon(QIcon('icon.png'))
        self.center()
        self.adjust_layout_direction(self.language)
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
        self.btn_fw.setGeometry(QtCore.QRect(0, 20, 161, 30))
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
        self.status_label.setGeometry(QtCore.QRect(0, 30, 580, 51))
        self.status_label.setFrameShape(QtWidgets.QFrame.Box)
        self.status_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.status_label.setLineWidth(2)
        self.status_label.setText("")
        self.status_label.setObjectName("status_label")
        # Action
        self.btn_select.clicked.connect(self.select_file)

    def menu_bar(self, main_window):
        """
        Menubar
        """
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 32))
        self.menubar.setObjectName("menubar")
        self.menu_file.setObjectName("menu_file")
        self.menu_language.setObjectName("menu_language")
        self.menu_help.setObjectName("menu_help")
        main_window.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.action_open_zip.setObjectName("action_open_zip")
        self.action_quit.setObjectName("action_quit")
        self.action_quit.setStatusTip("action_quit_tip")
        self.action_language_en.setObjectName("action_language_en")
        self.action_language_ar.setObjectName("action_language_ar")
        self.action_help.setObjectName("action_help")
        self.action_donate.setObjectName("action_donate")
        self.action_about.setObjectName("action_about")
        self.action_report_bug.setObjectName("action_report_bug")
        self.menu_file.addAction(self.action_open_zip)
        self.menu_file.addAction(self.action_quit)
        self.menu_language.addAction(self.action_language_en)
        self.menu_language.addAction(self.action_language_ar)
        self.menu_help.addAction(self.action_help)
        self.menu_help.addAction(self.action_report_bug)
        self.menu_help.addAction(self.action_donate)
        self.menu_help.addAction(self.action_about)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_language.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        # Shortcuts
        self.action_open_zip.setShortcut('Ctrl+O')
        self.action_quit.setShortcut('Ctrl+Q')
        # Actions
        self.action_open_zip.triggered.connect(self.select_file)
        self.action_quit.triggered.connect(qApp.quit)
        self.action_language_en.triggered.connect(lambda: self.change_language(main_window, "en"))
        self.action_language_ar.triggered.connect(lambda: self.change_language(main_window, "ar"))

    def retranslate_ui(self, main_window):
        """
        Items strings
        """
        _translate = QApplication.translate
        main_window.setWindowTitle(_translate("main_window", self.strings['main_window']))
        self.process_type.setTitle(_translate("process_type", self.strings['process_type']))
        self.btn_fw.setText(_translate("btn_fw", self.strings['btn_fw']))
        self.btn_nonarb.setText(_translate("btn_nonarb", self.strings['btn_nonarb']))
        self.btn_vendor.setText(_translate("btn_vendor", self.strings['btn_vendor']))
        self.btn_fwless.setText(_translate("btn_fwless", self.strings['btn_fwless']))
        self.groupbox_drop.setTitle(_translate("groupbox_drop", self.strings['groupbox_drop']))
        self.label_drop.setText(_translate("label_drop", self.strings['label_drop']))
        self.btn_select.setText(_translate("btn_select", self.strings['btn_select']))
        self.btn_create.setText(_translate("btn_create", self.strings['btn_create']))
        self.status_box.setTitle(_translate("status_box", self.strings['status_box']))
        self.menu_file.setTitle(_translate("menu_file", self.strings['menu_file']))
        self.menu_help.setTitle(_translate("menu_help", self.strings['menu_help']))
        self.menu_language.setTitle(_translate("menu_language", self.strings['menu_language']))
        self.action_open_zip.setText(_translate("action_open_zip", self.strings['action_open_zip']))
        self.action_quit.setText(_translate("action_quit", self.strings['action_quit']))
        self.action_quit.setStatusTip(_translate("action_quit_tip",
                                                 self.strings['action_quit_tip']))
        self.action_language_en.setText(_translate("action_language_en",
                                                   self.strings['action_language_en']))
        self.action_language_ar.setText(_translate("action_language_ar",
                                                   self.strings['action_language_ar']))
        self.action_help.setText(_translate("action_help", self.strings['action_help']))
        self.action_donate.setText(_translate("action_donate", self.strings['action_donate']))
        self.action_about.setText(_translate("action_about", self.strings['action_about']))
        self.action_report_bug.setText(_translate("action_report_bug",
                                                  self.strings['action_report_bug']))

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

    def change_language(self, main_window, lang: str):
        """
        Update strings language and settings
        """
        self.settings.update({'language': lang})
        update_settings(self.settings)
        self.language = self.settings['language']
        self.strings = self.translations[self.language]
        self.adjust_layout_direction(lang)
        self.retranslate_ui(main_window)

    def adjust_layout_direction(self, lang: str):
        """
        Change Layout Direction based on languages
        """
        if lang in RTL_LANGUAGES:
            self.setLayoutDirection(QtCore.Qt.RightToLeft)
        else:
            self.setLayoutDirection(QtCore.Qt.LeftToRight)

    def select_file(self):
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(self, 'Select MIUI zip', '', "MIUI zip files (miui*.zip)")[0]
        self.filepath = filepath
        self.filename = filepath.split('/')[-1]
        self.status_label.setText(f"File {self.filename} is selected")


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    WINDOW = MainWindowUi()
    sys.exit(APP.exec_())
