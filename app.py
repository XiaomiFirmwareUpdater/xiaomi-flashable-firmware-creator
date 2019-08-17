#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""Xiaomi Flashable Firmware Creator GUI"""

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QMimeDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, qApp, QFileDialog, QGroupBox
from PyQt5.QtGui import QIcon
from helpers.settings import load_settings, update_settings
import create_flashable_firmware as cf


class DropSpace(QGroupBox):
    """
    Modified Groupbox to allow drag and drop
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

    @classmethod
    def dragEnterEvent(cls, file):
        """
        Override default dragEnterEvent
        Allows dragging zip files only
        """
        file_type = QMimeDatabase().mimeTypeForFile(
            file.mimeData().urls()[0].toLocalFile()).name()
        if file_type == 'application/zip':
            file.accept()
        else:
            file.ignore()

    @classmethod
    def dropEvent(cls, file):
        """
        Override default dropEvent
        Update selected filename
        """
        filepath = file.mimeData().urls()[0].toLocalFile()
        WINDOW.filepath = filepath
        WINDOW.filename = filepath.split('/')[-1]
        WINDOW.status_box.setText(f"File {WINDOW.filename} is selected")


class MainWindowUi(QMainWindow):
    """Main Window"""
    def __init__(self):
        super(MainWindowUi, self).__init__()
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
        self.menubar = QtWidgets.QMenuBar(self)
        self.status_box = QtWidgets.QTextEdit(self.window_body)
        self.progress_bar = QtWidgets.QProgressBar(self.window_body)
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
        self.adjust_layout_direction(LANG)
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
        self.process_type.setGeometry(QtCore.QRect(10, 20, 160, 140))
        self.process_type.setObjectName("process_type")
        self.btn_fw.setGeometry(QtCore.QRect(0, 20, 160, 30))
        self.btn_fw.setObjectName("btn_fw")
        self.btn_nonarb.setGeometry(QtCore.QRect(0, 50, 160, 30))
        self.btn_nonarb.setObjectName("btn_nonarb")
        self.btn_vendor.setGeometry(QtCore.QRect(0, 80, 160, 30))
        self.btn_vendor.setObjectName("btn_vendor")
        self.btn_fwless.setGeometry(QtCore.QRect(0, 110, 160, 30))
        self.btn_fwless.setObjectName("btn_fwless")
        # Actions
        self.btn_fw.setChecked(True)

    def file_dropper(self):
        """
        GroupBox: Drop files
        """
        self.groupbox_drop.setGeometry(QtCore.QRect(195, 20, 390, 140))
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
        self.frame.setGeometry(QtCore.QRect(10, 170, 580, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.btn_select.setGeometry(QtCore.QRect(175, 20, 105, 35))
        self.btn_select.setObjectName("btn_select")
        self.btn_create.setGeometry(QtCore.QRect(290, 20, 105, 35))
        self.btn_create.setObjectName("btn_create")
        self.status_box.setGeometry(QtCore.QRect(10, 250, 580, 40))
        self.status_box.setObjectName("status_box")
        self.status_box.setFrameShape(QtWidgets.QFrame.Box)
        self.status_box.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.status_box.setReadOnly(True)
        self.status_box.setOverwriteMode(True)
        self.status_box.setObjectName("status_box")
        self.status_box.setText("Ready")
        self.progress_bar.setGeometry(QtCore.QRect(10, 300, 580, 40))
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setValue(0)

        # Action
        self.btn_select.clicked.connect(self.select_file)
        self.btn_create.clicked.connect(self.create_zip)

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
        self.action_language_en.triggered.connect(
            lambda: self.change_language(main_window, "en_US"))
        self.action_language_ar.triggered.connect(
            lambda: self.change_language(main_window, "ar"))

    def retranslate_ui(self, main_window):
        """
        Items strings
        """
        _translate = QApplication.translate
        main_window.setWindowTitle(_translate("Title",
                                              "Xiaomi Flashable Firmware Creator "
                                              "by XiaomiFirmwareUpdater"))
        self.process_type.setTitle(_translate("Radio Buttons", "Process"))
        self.btn_fw.setText(_translate("Radio Buttons", "Firmware"))
        self.btn_nonarb.setText(_translate("Radio Buttons", "Non-ARB Firmware"))
        self.btn_vendor.setText(_translate("Radio Buttons", "Firmware + Vendor"))
        self.btn_fwless.setText(_translate("Radio Buttons", "Firmware-less ROM"))
        self.groupbox_drop.setTitle(_translate("Drop space", "Drop a file"))
        self.label_drop.setText(_translate("Drop space",
                                           "<html><head/><body>"
                                           "<p align=\"center\">"
                                           "<span style=\" font-style:italic;\">"
                                           "Drop a rom zip file here"
                                           "</span></p></body></html>"))
        self.btn_select.setText(_translate("Main Buttons", "Select file"))
        self.btn_create.setText(_translate("Main Buttons", "Create"))
        self.menu_file.setTitle(_translate("Menu bar", "File"))
        self.menu_language.setTitle(_translate("Menu bar", "Language"))
        self.menu_help.setTitle(_translate("Menu bar", "Help"))
        self.action_open_zip.setText(_translate("Menu bar", "Open ZIP"))
        self.action_quit.setText(_translate("Menu bar", "Quit"))
        self.action_quit.setStatusTip(_translate("Menu bar", "Exits the application"))
        self.action_language_en.setText(_translate("Menu bar", "English"))
        self.action_language_ar.setText(_translate("Menu bar", "Arabic"))
        self.action_help.setText(_translate("Menu bar", "What\'s This?"))
        self.action_donate.setText(_translate("Menu bar", "Donate"))
        self.action_about.setText(_translate("Menu bar", "About"))
        self.action_report_bug.setText(_translate("Menu bar", "Report Bug"))

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
        update_settings(dict({'language': lang}))
        self.adjust_layout_direction(lang)
        TRANSLATOR.load(f'i18n/{lang}.qm')
        self.retranslate_ui(main_window)

    def adjust_layout_direction(self, lang: str):
        """
        Change Layout Direction based on languages
        """
        rtl_languages = ['ar']
        if lang in rtl_languages:
            self.setLayoutDirection(QtCore.Qt.RightToLeft)
        else:
            self.setLayoutDirection(QtCore.Qt.LeftToRight)

    def select_file(self):
        """
        Opens select file Dialog
        """
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(self, 'Select MIUI zip',
                                          '', "MIUI zip files (miui*.zip)")[0]
        self.filepath = filepath
        self.filename = filepath.split('/')[-1]
        self.status_box.setText(f"File {self.filename} is selected")

    def create_zip(self):
        """
        creates output zip file
        """
        checked_radiobutton = None
        process = None

        for button in self.process_type.findChildren(QtWidgets.QRadioButton):
            if button.isChecked():
                checked_radiobutton = button.text()
        if checked_radiobutton == 'Firmware':
            process = 'firmware'
        elif checked_radiobutton == 'Non-ARB Firmware':
            process = 'nonarb'
        elif checked_radiobutton == 'Firmware + Vendor':
            process = 'vendor'
        elif checked_radiobutton == 'Firmware-less ROM':
            process = 'firmwareless'
        self.status_box.setText(f"Starting {process} job")
        self.progress_bar.setValue(1)
        cf.init()
        self.progress_bar.setValue(5)
        fw_type = cf.firmware_type(self.filepath)
        self.status_box.setText(f"Detected {fw_type} device")
        self.progress_bar.setValue(10)
        if fw_type == 'qcom':
            if process == "firmware":
                self.status_box.setText(f"Unzipping MIUI... ({fw_type}) device")
                self.progress_bar.setValue(30)
                cf.firmware_extract(self.filepath, process)
                self.progress_bar.setValue(45)
                self.status_box.setText("Generating updater-script...")
                self.progress_bar.setValue(55)
                cf.firmware_updater()
            elif process == "nonarb":
                self.status_box.setText(f"Unzipping MIUI...")
                self.progress_bar.setValue(30)
                cf.firmware_extract(self.filepath, process)
                self.progress_bar.setValue(45)
                self.status_box.setText("Generating updater-script...")
                self.progress_bar.setValue(55)
                cf.nonarb_updater()
            elif process == "firmwareless":
                self.status_box.setText(f"Unzipping MIUI... ({fw_type}) device")
                self.progress_bar.setValue(30)
                cf.rom_extract(self.filepath)
                self.progress_bar.setValue(45)
                self.status_box.setText("Generating updater-script...")
                self.progress_bar.setValue(55)
                cf.firmwareless_updater()
            elif process == "vendor":
                self.status_box.setText(f"Unzipping MIUI... ({fw_type}) device")
                self.progress_bar.setValue(30)
                cf.vendor_extract(self.filepath)
                self.progress_bar.setValue(45)
                self.status_box.setText("Generating updater-script...")
                self.progress_bar.setValue(55)
                cf.vendor_updater()
        elif fw_type == 'mtk':
            if process == "firmware":
                self.status_box.setText(f"Unzipping MIUI... ({fw_type}) device")
                self.progress_bar.setValue(30)
                cf.mtk_firmware_extract(self.filepath)
                self.progress_bar.setValue(45)
                self.status_box.setText("Generating updater-script...")
                self.progress_bar.setValue(55)
                cf.mtk_firmware_updater()
            elif process == "vendor":
                self.status_box.setText(f"Unzipping MIUI... ({fw_type}) device")
                self.progress_bar.setValue(30)
                cf.vendor_extract(self.filepath)
                self.progress_bar.setValue(45)
                self.status_box.setText("Generating updater-script...")
                self.progress_bar.setValue(55)
                cf.mtk_vendor_updater()
            else:
                self.status_box.setText("Error: Unsupported operation for MTK!")
        else:
            self.status_box.setText("Couldn't find firmware!")
        self.status_box.setText("Creating zip..")
        self.progress_bar.setValue(75)
        cf.make_zip(self.filepath, process)
        self.status_box.setText("All Done!")
        self.progress_bar.setValue(100)


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    SETTINGS = load_settings()
    LANG = SETTINGS['language']
    TRANSLATOR = QtCore.QTranslator(APP)
    TRANSLATOR.load(f'i18n/{LANG}.qm')
    APP.installTranslator(TRANSLATOR)
    WINDOW = MainWindowUi()
    sys.exit(APP.exec_())
