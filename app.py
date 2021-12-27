# -*- coding: utf-8 -*-
import os.path
import subprocess
import urllib.request
import zipfile
from sys import exc_info
from traceback import extract_tb
import webbrowser
import requests
import winapps
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from igruha import Igruha

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
        down_url = 'https://github.com/LORD-ME-CODE/XGames/releases/download/v{}/XGames.zip'.format(APP_VERSION)
        save_loc = '../XGames {}.zip'.format(str(VERSION).replace('.', '_'))
        urllib.request.urlretrieve(down_url, save_loc, self.handle_progress)

        with zipfile.ZipFile(save_loc) as zf:
            self.progressbar.setMaximum(len(zf.infolist()))
            x = 0
            for member in zf.infolist():
                x += 1
                self.progressbar.setValue(x)
                try:
                    zf.extract(member, '../XGames {}/'.format(str(VERSION).replace('.', '_')))
                except zipfile.error as e:
                    print(e)
        try:
            os.remove('../XGames {}.zip'.format(str(VERSION).replace('.', '_')))
        except Exception as e:
            print(e)
        open('version', 'w', encoding='utf-8').write(str(VERSION))
        try:
            os.removedirs('../XGames {}/'.format(str(APP_VERSION).replace('.', '_')))
        except Exception as e:
            print(e)
        self.hide()


def info_message(text):
    return QMessageBox.about(Window, "INFO", text)


def warn_message(text):
    return QMessageBox.warning(Window, "WARN", text)


def error_message(text):
    return QMessageBox.warning(Window, "ERROR", text)


class MyWindow(object):
    def __init__(self):
        self.path = None
        self.last_game_label = None
        self.last_game = None
        self.games_widgets = []
        self.background = None
        self.search_game = None
        self.centralwidget = None
        self.torrent_url = None
        self.parser = Igruha()
        self.search_btn = None
        self.games_area = None
        self.games_content = None
        self.games_list = None

    def setup_ui(self, window):
        window.setObjectName("Window")
        window.resize(1093, 680)
        window.setWindowTitle("XGames")
        icon = QtGui.QIcon()
        icon.addFile('img/48x48.png', QtCore.QSize(48, 48))
        icon.addFile('img/16x16.png', QtCore.QSize(16, 16))
        icon.addFile('img/24x24.png', QtCore.QSize(24, 24))
        icon.addFile('img/32x32.png', QtCore.QSize(32, 32))
        icon.addFile('img/180x180.png', QtCore.QSize(180, 180))
        icon.addFile('img/192x192.png', QtCore.QSize(192, 192))
        icon.addFile('img/256x256.png', QtCore.QSize(256, 256))
        icon.addFile('img/512x512.png', QtCore.QSize(512, 512))
        window.setWindowIcon(icon)
        window.setFixedSize(1093, 680)

        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("""background-color: 
        qlineargradient(spread:pad, x1:0, y1:0.512, x2:0.985, y2:0.511, stop:0 rgba(255, 153, 0, 255),
         stop:1 rgba(255, 159, 255, 255));""")
        self.search_game = QtWidgets.QLineEdit(self.centralwidget)
        self.search_game.setGeometry(QtCore.QRect(20, 10, 911, 31))
        self.search_game.setStyleSheet("QLineEdit {\n"
                                       "border: 0.5px solid green;\n"
                                       "border-radius: 9px;\n"
                                       "background-color: white;\n"
                                       "font: 63 8pt \"Segoe UI Variable Small Semibol\";\n"
                                       "color: black;\n"
                                       "} QLineEdit:hover {\n"
                                       "border: 1px solid black;\n"
                                       "}")
        self.search_game.setText("")
        self.search_game.setAlignment(QtCore.Qt.AlignCenter)
        self.search_game.setPlaceholderText("Введите название игры...")
        self.search_game.setObjectName("search_game")
        self.search_btn = QtWidgets.QPushButton(self.centralwidget)
        self.search_btn.setGeometry(QtCore.QRect(940, 10, 141, 31))
        self.search_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_btn.setStyleSheet("QPushButton {\n"
                                      "    background-color: lime;\n"
                                      "    color: black;\n"
                                      "    font: 63 8pt \"Segoe UI Variable Small Semibol\";\n"
                                      "    border-radius: 9px;\n"
                                      "} QPushButton:hover {\n"
                                      "    border: 1px solid dark;\n"
                                      "    background-color: green;\n"
                                      "}")
        self.search_btn.setText("Найти")
        self.search_btn.setObjectName("search_btn")
        self.search_btn.clicked.connect(self.search)
        self.games_area = QtWidgets.QScrollArea(self.centralwidget)
        self.games_area.setGeometry(QtCore.QRect(20, 50, 1061, 621))
        self.games_area.setStyleSheet("background: transparent;"
                                      "border: none;")
        self.games_area.setWidgetResizable(True)
        self.games_area.setObjectName("games_area")
        self.games_content = QtWidgets.QWidget()
        self.games_content.setGeometry(QtCore.QRect(0, 0, 1059, 619))
        self.games_content.setObjectName("games_content")
        self.games_content.setStyleSheet("border: none;\nbackground: transparent;\n"
                                         "font: 63 9pt \"Cascadia Code SemiBold\";")

        self.games_area.verticalScrollBar().setStyleSheet("QScrollBar"
                                                          "{"
                                                          "border: none;"
                                                          "background: transparent;"
                                                          "}"
                                                          "QScrollBar::handle"
                                                          "{"
                                                          "background: #868687;"
                                                          "border-radius: 10px;"
                                                          "border: none;"
                                                          "}"
                                                          "QScrollBar::handle::pressed"
                                                          "{"
                                                          "background: white;"
                                                          "}"
                                                          """
QScrollBar::handle:vertical {
border-radius: 10px;
border: none;
background: #5b5b5b;
} QScrollBar::handle:vertical::pressed {
background: lightgray;
}

QScrollBar::add-line:vertical {
height: 0px;
}

QScrollBar::sub-line:vertical {
height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
height: 0px;
background: none;
border-radius: 14px;
}""")

        self.games_area.setWidget(self.games_content)

        self.games_list = []

        self.search_game.raise_()
        self.search_btn.raise_()

        self.games_area.setWidgetResizable(True)

        self.games_area.raise_()

        window.setCentralWidget(self.centralwidget)

        self.search_btn.setShortcut("Return")
        QtCore.QMetaObject.connectSlotsByName(window)

        self.search_main()

    def search_main(self):
        try:
            self.games_list = self.parser.main_games().games
            for i in set(self.games_list):
                if 'vazhnaya-informaciya' in i.link or 'ПРИЛОЖЕНИЕ' in i.name:
                    self.games_list.remove(i)
                elif i.img.startswith('/'):
                    i.img = 'https://q.itorrents-igruha.org' + i.img
            self.update_games()
        except (AttributeError, IndexError):
            return error_message('Произошла ошибка:\n' + 'Не удалось найти ниодной игры!')
        except Exception as e:
            return error_message('Произошла ошибка:\n' + str(e) + '\n' + str(extract_tb(exc_info()[2])[0][1]))

    def search(self):
        try:
            try:
                [(i[0].hide(), i[1].hide()) for i in self.games_widgets]
            except Exception as e:
                print(e)
            game = self.search_game.text().replace('\n', '')
            if len(game) < 3:
                return warn_message('Введите более 3-х символов!')
            self.games_list = list(set(self.parser.search(game).games))
            self.update_games()
        except AttributeError:
            return error_message('Произошла ошибка:\n' + 'Не удалось найти ниодной игры!')
        except Exception as e:
            return error_message('Произошла ошибка:\n' + str(e) + '\n' + str(extract_tb(exc_info()[2])[0][1]))

    def make_lambda(self, game):
        def setup():
            self.dialog_game(game)
        return setup

    def make_lambda2(self, game):
        def setup():
            self.download_game(game)
        return setup

    def update_games(self):
        self.path = os.getenv('TEMP') + '\\XGames\\'
        try:
            os.makedirs(self.path)
        except Exception as e:
            print(e)

        z = 1
        x, y = 20, 10

        ww = round((len(self.games_list) / 5) * 350) + 350

        self.games_content.setFixedHeight(ww)

        for i in enumerate(self.games_list):
            setattr(self, 'game%d' % i[0], QtWidgets.QPushButton(self.games_content))
            self.last_game = getattr(self, 'game%d' % i[0])
            self.last_game.clicked.connect(self.make_lambda(i[1]))
            self.last_game.setGeometry(QtCore.QRect(x, y, 175, 240))
            self.last_game.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

            setattr(self, 'game%d_label' % i[0], QtWidgets.QLabel(self.games_content))
            self.last_game_label = getattr(self, 'game%d_label' % i[0])
            self.last_game_label.setGeometry(QtCore.QRect(x, y + 240, 175, 50))

            x += 205
            if z % 5 == 0:
                x = 20
                y += 298

            self.last_game_label.setText(i[1].name)
            self.last_game_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
            self.last_game_label.setWordWrap(True)

            name = i[1].name
            name = name.replace(' ', '_').replace('\'', '')
            name = name.replace('.', '_').replace('/', '_')
            name = name.replace('\\', '_')

            url = self.path + name + '.'
            url = url.replace('\\', '/')

            if '.jpg' in i[1].img:
                url += 'jpg'
            elif '.jpeg' in i[1].img:
                url += 'jpeg'
            else:
                url += 'png'

            if not os.path.isfile(url):
                open(url, 'wb').write(requests.get(i[1].img).content)

            self.last_game.setStyleSheet("QPushButton {\n"
                                         "border: 1px solid black;\n"
                                         "background-color: rgba(255,255,255,0);\n"
                                         f"border-image: url({url}) 0 0 0 0 stretch stretch;"
                                         "border-radius: 12px"
                                         "} QPushButton:hover {\n"
                                         ";"
                                         "margin-top: 5px;"
                                         "}")

            self.last_game.show()
            self.last_game_label.show()

            self.games_widgets.append([self.last_game, self.last_game_label])

            z += 1

    def download_game(self, game):
        if 'itorrents-igruha' not in game.link:
            return webbrowser.open(game.link)
        name = game.game_name.replace('\'', '').replace(' ', '_')

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            Window, 'Save Torrent', name + '.torrent', "Torrent File (*.torrent)"
        )

        if filename == "":
            return

        try:
            game.download(filename.replace('.torrent', ''))
        except Exception as e:
            return error_message('Произошла ошибка:\n' + str(e))

        info_message('Торрент успешно закачан по пути:\n' + filename)

        if self.torrent_url is None:
            for programm in winapps.list_installed():
                if 'torrent' in programm.name.lower():
                    self.torrent_url = programm.install_location
                    if self.torrent_url is None:
                        continue
        if self.torrent_url:
            return subprocess.call(['"{}"'.format(str(self.torrent_url)), filename])
        else:
            a = filename.split('/')
            a.remove(a[-1])
            return os.startfile('/'.join(a))

    def dialog_game(self, game):
        if game.id is None:
            try:
                if game.link.startswith('/'):
                    game.link = 'https://q.itorrents-igruha.org' + game.link
                game = game.get_details()
            except IndexError:
                return error_message('Произошла ошибка:\nТоррентов не найдено!')
            except Exception as e:
                return error_message('Произошла ошибка:\n' + str(e))
        y = 20

        dialog = QtWidgets.QDialog(self.centralwidget)
        dialog.resize(600, 400)
        dialog.setWindowTitle("XGames | Download")
        dialog.setFixedSize(600, 400)
        widget = QtWidgets.QWidget(dialog)
        widget.setFixedHeight(400)
        widget.setFixedWidth(600)
        widget.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,'
                             ' stop:0 rgba(255, 0, 255, 255), stop:1 rgba(158, 0, 255, 255));')

        req = QtWidgets.QPushButton(widget)
        req.setStyleSheet("""
QPushButton {
    background-color: yellow;
    border-radius: 10px;
    font: 7pt;
} QPushButton:hover {
    border: 1px solid black;
    margin-left: 5px;
    margin-top: 5px;
}
""")
        req.setText('С\nи\nс\nт\nе\nм\nн\nы\nе\n\nт\nр\nе\nб\nо\nв\nа\nн\nи\nя')
        req.clicked.connect(self.make_lambda3(game, 'requirements'))
        req.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        req.setGeometry(QtCore.QRect(5, 5, 40, 390))

        req.raise_()
        req.show()

        info = QtWidgets.QPushButton(widget)
        info.setStyleSheet("""
QPushButton {
    background-color: blue;
    border-radius: 10px;
    font: 7pt;
} QPushButton:hover {
    border: 1px solid black;
    margin-left: 5px;
    margin-top: 5px;
}
""")
        info.setText('О\nп\nи\nс\nа\nн\nи\nе')
        info.clicked.connect(self.make_lambda3(game, 'info'))
        info.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        info.setGeometry(QtCore.QRect(50, 5, 40, 390))

        info.raise_()
        info.show()

        for i in enumerate(game.torrents):
            setattr(self, 'torrent%d' % i[0], QtWidgets.QPushButton(widget))
            game = getattr(self, 'torrent%d' % i[0])
            game.setGeometry(QtCore.QRect(150, y, 300, 60))
            game.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            game.clicked.connect(self.make_lambda2(i[1]))
            game.setStyleSheet("""
QPushButton {
    background-color: lime;
    border-radius: 19px;
} QPushButton:hover {
    border: 1px solid black;
    border-radius: 21px;
    margin-top: 5px;
}
""")

            game.setText(i[1].name)

            y += 80

            game.raise_()
            game.show()

        widget.raise_()
        widget.show()

        dialog.setWindowState(QtCore.Qt.WindowActive)
        dialog.showNormal()
        dialog.activateWindow()
        dialog.raise_()

        return dialog.show()

    def make_lambda3(self, game, text):
        def setup():
            self.dialog_info(game, text)
        return setup

    def dialog_info(self, game, texts):
        if game.requirements is None:
            return error_message('К сожалению к игре нет системных требований на сайте!')
        dialog = QtWidgets.QDialog(self.centralwidget)
        dialog.resize(600, 400)
        dialog.setFixedSize(600, 400)
        dialog.setWindowTitle("XGames | Доп.Инфа")
        widget = QtWidgets.QWidget(dialog)

        text = QtWidgets.QLabel(widget)
        text.setWordWrap(True)
        text.setFixedWidth(600)
        text.setFixedHeight(400)
        text.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)

        if texts == 'requirements':
            texts = str(game.requirements)
        elif texts == 'info':
            texts = str(game.description)

        text.setText(texts)

        widget.raise_()
        widget.show()

        dialog.setWindowState(QtCore.Qt.WindowActive)
        dialog.showNormal()
        dialog.activateWindow()
        dialog.raise_()

        return dialog.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    if APP_VERSION != VERSION:
        DownloadWidget().download()
    Window = QtWidgets.QMainWindow()
    ui = MyWindow()
    ui.setup_ui(Window)
    Window.show()
    sys.exit(app.exec_())
