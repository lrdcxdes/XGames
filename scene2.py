import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox

from games import Games

GAMES = Games()


class Label(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self, *args, **kwargs)

    def enterEvent(self, event):
        self.setStyleSheet('text-decoration: underline;')

    def leaveEvent(self, event):
        self.setStyleSheet('text-decoration: none;')


class Button(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)

        self.lb_pressed = lambda: print(1)
        self.rb_pressed = lambda: print(1)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.lb_pressed()
        elif event.button() == QtCore.Qt.RightButton:
            self.rb_pressed()


class Scene2(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.warn_text = None
        self.progressbar = None
        self.last_game_label = None
        self.last_game = None
        self.games_list = None
        self.games_content = None
        self.games_area = None
        self.games_widgets = []
        self.game_state = {}
        self.lenghts = (sum(1 for _ in os.walk(drv)) for drv in (chr(i) + ":\\" for i in
                                                                 range(ord("A"),
                                                                       ord("Z") + 1)))
        self.lenght = None

    def setup_ui(self):
        self.resize(1093, 680)
        self.setFixedSize(1093, 680)

        self.setStyleSheet("""background-color: 
                qlineargradient(spread:pad, x1:0, y1:0.512, x2:0.985, y2:0.511, stop:0 rgba(255, 153, 0, 255),
                 stop:1 rgba(255, 159, 255, 255));""")

        self.progressbar = QtWidgets.QProgressBar(self)
        self.progressbar.setValue(0)
        self.progressbar.setGeometry(QtCore.QRect(10, 650, 1073, 20))

        self.warn_text = QtWidgets.QLabel(self)
        self.warn_text.setGeometry(QtCore.QRect(10, 10, 1093, 40))
        self.warn_text.setText('Используйте <b>ЛКМ</b> чтобы запустить игру или <b>ПКМ</b> чтобы удалить игру')
        self.warn_text.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
        self.warn_text.setWordWrap(True)
        self.warn_text.setStyleSheet('background: transparent;'
                                     'font: 12pt "Minecraft Rus";')

        self.games_area = QtWidgets.QScrollArea(self)
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

        self.games_area.setWidgetResizable(True)

        self.games_area.raise_()

        self.show()

        self.main()

    def make_lambda(self, game):
        def setup(*args):
            self.open_game(game)

        return setup

    def make_lambda_delete(self, game):
        def setup():
            self.delete_game(game)

        return setup

    def main(self):
        [(i[0].hide(), i[1].hide()) for i in self.games_widgets]
        self.games_widgets = []
        self.games_list = GAMES.reload().games

        z = 1
        x, y = 20, 10

        ww = round((len(self.games_list) / 5) * 350) + 350

        self.games_content.setFixedHeight(ww)

        for i in enumerate(GAMES.games):
            setattr(self, 'game%d' % i[0], Button(self.games_content))
            self.last_game = getattr(self, 'game%d' % i[0])
            self.last_game.lb_pressed = self.make_lambda(i[1])
            self.last_game.rb_pressed = self.make_lambda_delete(i[1])
            self.last_game.setGeometry(QtCore.QRect(x, y, 175, 240))
            self.last_game.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

            setattr(self, 'game%d_label' % i[0], Label(self.games_content))
            self.last_game_label = getattr(self, 'game%d_label' % i[0])
            self.last_game_label.setGeometry(QtCore.QRect(x, y + 240, 175, 50))

            x += 205
            if z % 5 == 0:
                x = 20
                y += 298

            self.last_game_label.setText(i[1].name)
            self.last_game_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
            self.last_game_label.setWordWrap(True)
            self.last_game_label.mousePressEvent = self.make_lambda(i[1])

            url = i[1].img

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

    def handle(self, i, maximum):
        self.progressbar.setMaximum(maximum)
        self.progressbar.setValue(i)
        QtWidgets.QApplication.processEvents()

    def find_exe(self, game):
        for drv in (chr(i) + ":\\" for i in range(ord("A"), ord("Z") + 1)):
            self.handle(50, 100)
            i = 0
            for root, dirs, files in os.walk(drv):
                i += 1
                if True in [game.name.lower() in i.lower() for i in files] and '.torrent' not in str(
                        files) and 'AppData' not in root and 'Documents' not in root and 'Документы' not in root:
                    return [root, files]
                self.handle(i, self.lenght)
        return False

    def delete_game(self, game):
        game.remove()
        self.main()

    def open_game(self, game):
        if self.game_state:
            return
        if not game.exe:
            self.game_state = True
            if self.lenght is None:
                self.lenght = sum(self.lenghts)
            exe = self.find_exe(game)
            self.game_state = False
            self.handle(0, 100)
            if exe:
                for i in exe[1]:
                    if game.name in i and 'деинстал' not in i.lower() and 'unin' not in i.lower():
                        path = exe[0] + '\\' + i
                        game.exe = path.replace('/', '\\')
                    elif 'деинст' in i.lower() or 'unins' in i.lower():
                        path = exe[0] + '\\' + i
                        game.uninstall_exe = path.replace('/', '\\')
                    game.update_game()
            else:
                return self.error_message('Вы не установили игру!')
        try:
            os.startfile(game.exe)
        except Exception as e:
            print(e)
            return self.error_message('Не удалось найти игру!')

    def info_message(self, text):
        return QMessageBox.about(self, "INFO", text)

    def warn_message(self, text):
        return QMessageBox.warning(self, "WARN", text)

    def error_message(self, text):
        return QMessageBox.warning(self, "ERROR", text)
