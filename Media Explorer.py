from PyQt5 import QtWidgets
from src.builds.ui_mainwindow import Ui_MainWindow
from src.MediaPlayerWidget import MediaPlayerWidget
import sys


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.MediaPlayerWidget = MediaPlayerWidget(self.MediaPlayerContainer)
        self.MediaPlayerContainerLayout.addWidget(self.MediaPlayerWidget)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
