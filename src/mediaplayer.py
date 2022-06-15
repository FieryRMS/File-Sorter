from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from ui_mediaplayerwidget import Ui_MediaPlayerWidget
from pathlib import Path
import mpv

class MediaPlayetrWidget(QtWidgets.QWidget, Ui_MediaPlayerWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.VolumeSlider.setVisible(False)

        self.isVideo = False
        self.MediaContainer.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.MediaContainer.setAttribute(Qt.WA_NativeWindow)
        self.player = mpv.MPV(wid=str(int(self.MediaContainer.winId())))
        self.player.pause=True
        self.PlayMedia(r"test_files\redditsave.com_st-ty0q9xmffe391-360.mp4")
        self.PlayPauseBtn.clicked['bool'].connect(self.play)

    def play(self, playing):
        self.player.pause=not playing
    
    def PlayMedia(self, FilePath: str):
        if(not Path(FilePath).is_file()):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('The specified file could not be opened')
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        if(FilePath.endswith(".mp4")):
            if(self.isVideo):
                    self.player.play(FilePath)
            else:
                self.player.play(FilePath)
                self.isVideo=True



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MediaPlayerWidget = MediaPlayetrWidget()
    MediaPlayerWidget.show()
    sys.exit(app.exec_())
