# -*- coding: utf-8 -*-
import os.path
import subprocess
import sys
import urllib.request

import requests
from PyQt5 import QtWidgets, QtGui, QtCore

from scene1 import Scene1
from scene2 import Scene2

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

APP_VERSION = float(open('version', 'r', encoding='utf-8').readline().replace(' ', '').replace('\n', ''))

VERSION = float(requests.get(url='https://raw.githubusercontent.com/LORD-ME-CODE/XGames/main/version'
                             ).text.replace(' ', '').replace('\n', ''))


class DownloadWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.progressbar = None
        self.init_ui()

    def init_ui(self):
        self.progressbar = QtWidgets.QProgressBar(self)
        self.progressbar.setGeometry(25, 45, 210, 30)

        self.setGeometry(310, 310, 280, 170)

        self.setWindowTitle("UPDATE")

        self.show()

    def handle_progress(self, blocknum, blocksize, totalsize):
        self.progressbar.setMaximum(totalsize)
        self.progressbar.setValue(0)
        readed_data = blocknum * blocksize
        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressbar.setValue(download_percentage)
            QtWidgets.QApplication.processEvents()
        self.progressbar.setValue(0)

    def download(self):
        down_url = 'https://github.com/LORD-ME-CODE/XGames/releases/download/setup/XGames.Setup.exe'
        save_loc = '../XGames Setup.exe'
        urllib.request.urlretrieve(down_url, save_loc, self.handle_progress)

        try:
            os.startfile(save_loc)
        except Exception as e:
            print(e)
            try:
                os.startfile('..')
            except Exception as e:
                print(e)

        sys.exit()


class Main(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.home = None
        self.palka = None
        self.btn = None
        self.scene2 = None
        self.scene1 = None
        self.scene = 1

    def setup_ui(self):
        self.setObjectName("Window")
        self.resize(1293, 680)
        self.setWindowTitle("XGames")
        icon = QtGui.QIcon()
        icon.addFile('img/48x48.png', QtCore.QSize(48, 48))
        icon.addFile('img/16x16.png', QtCore.QSize(16, 16))
        icon.addFile('img/24x24.png', QtCore.QSize(24, 24))
        icon.addFile('img/32x32.png', QtCore.QSize(32, 32))
        icon.addFile('img/180x180.png', QtCore.QSize(180, 180))
        icon.addFile('img/192x192.png', QtCore.QSize(192, 192))
        icon.addFile('img/256x256.png', QtCore.QSize(256, 256))
        icon.addFile('img/512x512.png', QtCore.QSize(512, 512))
        self.setWindowIcon(icon)
        self.setFixedSize(1293, 680)

        self.setStyleSheet("""background-color: 
                qlineargradient(spread:pad, x1:0, y1:0.512, x2:0.985, y2:0.511, stop:0 rgba(255, 153, 0, 255),
                 stop:1 rgba(255, 159, 255, 255));""")

        QtCore.QMetaObject.connectSlotsByName(self)

        self.palka = QtWidgets.QLabel(self)
        self.palka.setGeometry(QtCore.QRect(1090, 0, 4, 680))
        self.palka.setStyleSheet("""background-color: 
                gray""")

        self.btn = QtWidgets.QPushButton(self)
        self.btn.clicked.connect(self.lambdas)
        self.btn.setGeometry(QtCore.QRect(1100, 590, 185, 80))
        self.btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn.setStyleSheet("QPushButton {\n"
                               "    background: #aadd46;\n"
                               "    color: white;\n"
                               "    font: 63 10pt \"Segoe UI Variable Small Semibol\";\n"
                               "    border-radius: 9px;\n"
                               "} QPushButton:hover {\n"
                               "    background: #454545;\n"
                               "} QPushButton:pressed {\n"
                               "    background: #454545;\n"
                               "}")
        self.btn.setText("Поиск игр")

        self.scene1 = Scene1(self)
        self.scene1.setWindowIcon(icon)
        self.scene1.setup_ui()

        self.home = QtWidgets.QPushButton(self)
        self.home.clicked.connect(self.scene1.search_main)
        self.home.setGeometry(QtCore.QRect(1100, 10, 185, 80))
        self.home.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.home.setStyleSheet("QPushButton {\n"
                                "    background: #aadd46;\n"
                                "    color: white;\n"
                                "    font: 63 10pt \"Segoe UI Variable Small Semibol\";\n"
                                "    border-radius: 9px;\n"
                                "} QPushButton:hover {\n"
                                "    background: #454545;\n"
                                "} QPushButton:pressed {\n"
                                "    background: #454545;\n"
                                "}")
        self.home.setText("Главное меню")

        self.scene2 = Scene2(self)
        self.scene2.setWindowIcon(icon)
        self.scene2.setup_ui()

        self.scene2.hide()

        self.show()

    def lambdas(self):
        if self.scene == 1:
            self.scene2.main()
            self.scene2.show()
            self.scene1.hide()
            self.scene = 2
            self.btn.setText("Ваши игры")
        else:
            self.scene1.show()
            self.scene2.hide()
            self.btn.setText("Поиск игр")
            self.scene = 1
