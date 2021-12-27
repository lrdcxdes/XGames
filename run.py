from PyQt5 import QtWidgets
from app import APP_VERSION, VERSION, DownloadWidget, Main

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if APP_VERSION != VERSION:
        DownloadWidget().download()
    ui = Main()
    ui.setup_ui()
    sys.exit(app.exec_())
