from PyQt5 import QtWidgets
from src import ui_mainwindow
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MediaPlayerWidget = QtWidgets.QWidget()
    ui = ui_mainwindow.MainWindow()
    ui.setupUi(MediaPlayerWidget)
    ui.VolumeSlider.setHidden(True)
    MediaPlayerWidget.show()
    sys.exit(app.exec_())
