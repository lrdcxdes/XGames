# -*- coding: utf-8 -*-
import requests
import winapps
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWinExtras import QWinTaskbarButton
from igruha import Igruha
import os.path
from PyQt5.QtWidgets import QMessageBox
from sys import exc_info
from traceback import extract_tb
import subprocess


class Ui_Window(object):
    def __init__(self):
        self.torrent_url = None
        self.parser = Igruha()
        self.search_btn = None
        self.games_area = None
        self.games_content = None
        self.games_list = None

    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(1093, 680)
        Window.setWindowTitle("XGames")
        icon = QtGui.QIcon()
        #icon.addFile('img/favicon.ico', QtCore.QSize(48, 48))
        icon.addFile('img/48x48.png', QtCore.QSize(48, 48))
        icon.addFile('img/16x16.png', QtCore.QSize(16, 16))
        icon.addFile('img/24x24.png', QtCore.QSize(24, 24))
        icon.addFile('img/32x32.png', QtCore.QSize(32, 32))
        icon.addFile('img/180x180.png', QtCore.QSize(180, 180))
        icon.addFile('img/192x192.png', QtCore.QSize(192, 192))
        icon.addFile('img/256x256.png', QtCore.QSize(256, 256))
        icon.addFile('img/512x512.png', QtCore.QSize(512, 512))
        btn = QWinTaskbarButton(Window)
        btn.setOverlayIcon(icon)
        btn.setWindow(Window.windowHandle())
        Window.setWindowIcon(icon)
        Window.setFixedSize(1093, 680)

        self.centralwidget = QtWidgets.QWidget(Window)
        self.centralwidget.setObjectName("centralwidget")

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
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(-10, -10, 1111, 701))
        self.background.setStyleSheet("background-color: white;")
        self.background.setText("")
        self.background.setObjectName("background")
        self.games_area = QtWidgets.QScrollArea(self.centralwidget)
        self.games_area.setGeometry(QtCore.QRect(20, 50, 1061, 621))
        self.games_area.setStyleSheet("background-color: white;")
        self.games_area.setWidgetResizable(True)
        self.games_area.setObjectName("games_area")
        self.games_content = QtWidgets.QWidget()
        self.games_content.setGeometry(QtCore.QRect(0, 0, 1059, 619))
        self.games_content.setObjectName("games_content")

        self.games_area.verticalScrollBar().setStyleSheet("QScrollBar"
                                                          "{"
                                                          "background : lightgreen;"
                                                          "border-radius: 10px;"
                                                          "}"
                                                          "QScrollBar::handle"
                                                          "{"
                                                          "background : pink;"
                                                          "border-radius: 10px;"
                                                          "}"
                                                          "QScrollBar::handle::pressed"
                                                          "{"
                                                          "background : green;"
                                                          "border-radius: 10px;"
                                                          "}")

        self.games_area.setWidget(self.games_content)

        self.games_list = []

        self.games_widgets = []

        self.background.raise_()
        self.search_game.raise_()
        self.search_btn.raise_()

        self.games_area.setWidgetResizable(True)

        self.games_area.raise_()

        Window.setCentralWidget(self.centralwidget)

        self.search_btn.setShortcut("Return")
        QtCore.QMetaObject.connectSlotsByName(Window)

        self.search_main()

    def search_main(self):
        try:
            self.games_list = self.parser.main_games().games
            for i in self.games_list:
                if 'Важная информация' in i.name:
                    self.games_list.remove(i)
                elif i.img.startswith('/'):
                    i.img = 'https://q.itorrents-igruha.org' + i.img
            self.update_games()
        except AttributeError as e:
            return self.error_message('Произошла ошибка:\n' + 'Не удалось найти ниодной игры!')
        except Exception as e:
            return self.error_message('Произошла ошибка:\n' + str(e) + '\n' + str(extract_tb(exc_info()[2])[0][1]))

    def search(self):
        try:
            try:
                [(i[0].hide(), i[1].hide()) for i in self.games_widgets]
            except:
                pass
            game = self.search_game.text().replace('\n', '')
            if len(game) < 3:
                return self.warn_message('Введите более 3-х символов!')
            self.games_list = self.parser.search(game).games
            self.update_games()
        except AttributeError as e:
            return self.error_message('Произошла ошибка:\n' + 'Не удалось найти ниодной игры!')
        except Exception as e:
            return self.error_message('Произошла ошибка:\n' + str(e) + '\n' + str(extract_tb(exc_info()[2])[0][1]))

    def make_lambda(self, game):
        def setup():
            self.dialog_game(game)

        return setup

    def make_lambda2(self, game):
        def setup():
            self.download_game(game)

        return setup

    def update_games(self):
        z = 1
        x, y = 20, 10

        ww = round((len(self.games_list) / 5) * 334 ) + 334

        self.games_area.setMaximumHeight(ww)
        self.games_content.setFixedHeight(ww)

        path = os.getenv('TEMP') + '\\XGames\\'
        try:
            os.makedirs(path)
        except Exception as e:
            pass

        for i in enumerate(self.games_list):
            setattr(self, 'game%d' % i[0], QtWidgets.QPushButton(self.games_content))
            self.last_game = getattr(self, 'game%d' % i[0])
            self.last_game.clicked.connect(self.make_lambda(i[1]))
            self.last_game.setGeometry(QtCore.QRect(x, y, 175, 240))
            self.last_game.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

            self.last_game.setText("")
            self.last_game.setShortcut("")
            self.last_game.setObjectName("game%d" % i[0])
            setattr(self, 'game%d_label' % i[0], QtWidgets.QLabel(self.games_content))
            self.last_game_label = getattr(self, 'game%d_label' % i[0])
            self.last_game_label.setGeometry(QtCore.QRect(x, y + 240, 175, 42))

            x += 205
            if z % 5 == 0:
                x = 20
                y += 290

            self.last_game_label.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.last_game_label.setStyleSheet("color: black;\n"
                                               "background-color: rgba(255,255,255,0);\n"
                                               "font: 75 9pt \"Segoe UI\";")
            self.last_game_label.setText("%s" % i[1].name)
            self.last_game_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
            self.last_game_label.setObjectName("game%d_label" % i[0])
            self.last_game_label.setWordWrap(True)

            url = path + i[1].name + '.'
            url = url.replace('\\', '/')
            url = url.replace(' ', '_').replace('\'', '')

            if '.jpeg' in i[1].img:
                url += 'jpeg'
            elif '.jpg' in i[1].img:
                url += 'jpg'
            else:
                url += 'png'

            if not os.path.isfile(url):
                open(url, 'wb').write(requests.get(i[1].img).content)

            self.last_game.setStyleSheet("QPushButton {\n"
                                         "border: 1px solid black;\n"
                                         "background-color: rgba(255,255,255,0);\n"
                                         f"border-image: url({url}) 0 0 0 0 stretch stretch;"
                                         "} QPushButton:hover {\n"
                                         "border-radius: 12px;"
                                         "margin-top: 5px;"
                                         "}")

            self.last_game.raise_()
            self.last_game_label.raise_()

            self.last_game.show()
            self.last_game_label.show()

            self.games_widgets.append([self.last_game, self.last_game_label])

            z += 1

    def info_message(self, text):
        return QMessageBox.about(Window, "INFO", text)

    def warn_message(self, text):
        return QMessageBox.warning(Window, "WARN", text)

    def error_message(self, text):
        return QMessageBox.warning(Window, "ERROR", text)

    def download_game(self, game):
        name = game.game_name.replace('\'', '').replace(' ', '_')

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            Window, 'Save Torrent', name + '.torrent', "Torrent File (*.torrent)"
        )

        if filename == "":
            return

        try:
            game.download(filename.replace('.torrent', ''))
        except Exception as e:
            return self.error_message('Произошла ошибка:\n' + str(e))

        self.info_message('Торрент успешно закачан по пути:\n' + filename)

        if self.torrent_url is None:
            for app in winapps.list_installed():
                if 'torrent' in app.name.lower():
                    self.torrent_url = app.install_location
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
            except IndexError as e:
                return self.error_message('Произошла ошибка:\nТоррентов не найдено!')
            except Exception as e:
                return self.error_message('Произошла ошибка:\n' + str(e))
        y = 20

        dialog = QtWidgets.QDialog(Window)
        dialog.resize(600, 400)
        dialog.setWindowTitle("XGames | Download")
        dialog.setFixedSize(600, 400)
        widget = QtWidgets.QWidget(dialog)

        btn = QtWidgets.QPushButton(widget)
        btn.setStyleSheet("""
QPushButton {
    background-color: blue;
    border-radius: 10px;
} QPushButton:hover {
    border: 1px solid black;
    border-radius: 21px;
    margin-top: 5px;
}
""")
        btn.setText('Системные требования')
        btn.clicked.connect(self.make_lambda3(game))
        btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn.setGeometry(QtCore.QRect(2, 2, 150, 20))
        btn.raise_()
        btn.show()

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

    def make_lambda3(self, game):
        def setup():
            self.dialog_info(game)

        return setup

    def dialog_info(self, game):
        if game.requirements is None:
            return self.error_message('К сожалению к игре нет системных требований на сайте!')
        dialog = QtWidgets.QDialog(Window)
        dialog.resize(600, 400)
        dialog.setFixedSize(600, 400)
        dialog.setWindowTitle("XGames | Доп.Инфа")
        widget = QtWidgets.QWidget(dialog)

        text = QtWidgets.QLabel(widget)
        text.setWordWrap(True)
        text.setFixedWidth(600)
        text.setFixedHeight(400)

        text.setText(game.requirements)

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
    Window = QtWidgets.QMainWindow()
    ui = Ui_Window()
    ui.setupUi(Window)
    Window.show()
    sys.exit(app.exec_())
