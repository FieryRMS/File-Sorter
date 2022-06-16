if(1):
    import os
    os.environ['PATH'] += os.pathsep + os.path.abspath(
        'dlls/')
from pathlib import Path
from ui_mediaplayerwidget import Ui_MediaPlayerWidget
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QPoint, QRect
from PyQt5 import QtWidgets, QtGui
import mpv

class MediaPlayetrWidget(QtWidgets.QWidget, Ui_MediaPlayerWidget):
    percentpos = pyqtSignal(float, name="percentpos")
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.isVideo = False
        
        self.MediaContainer.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.MediaContainer.setAttribute(Qt.WA_NativeWindow)
        self.player = mpv.MPV(
            wid=str(int(self.MediaContainer.winId())),
        )
        self.UnPause(False)

        self.verticalLayout.removeWidget(self.VolumeSlider)
        self.VolumeSliderWrapper=QtWidgets.QDialog()
        self.VolumeSlider.setParent(self.VolumeSliderWrapper)
        self.VolumeSliderWrapper.setStyleSheet("background: transparent")
        self.VolumeSliderWrapper.setWindowFlags(
            Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Popup)
        self.VolumeSliderWrapper.setAttribute(Qt.WA_TranslucentBackground)
        
        self.VolumeBtn.clicked['bool'].connect(self.ShowVolumeSlider)
        self.VolumeSliderWrapper.closeEvent = self.UnselectVolumeBtnOnClose

        self.PlayPauseBtn.clicked['bool'].connect(self.UnPause)
        self.VolumeSlider.valueChanged['int'].connect(self.SetVolume)

    @pyqtSlot(bool)
    def UnPause(self, playing):
        self.player.pause = not playing

    @pyqtSlot(bool)
    def ShowVolumeSlider(self, checked):
        self.VolumeSliderWrapper.setVisible(checked)
        if(checked):
            p = self.VolumeBtn.mapToGlobal(QPoint(3, -130))
            self.VolumeSliderWrapper.move(p)
            self.VolumeBtn.setFocus()
    
    @pyqtSlot(int)
    def SetVolume(self, val):
        self.player.volume = val*100 / self.VolumeSlider.maximum()




    def UnselectVolumeBtnOnClose(self, e):
        p = self.VolumeBtn.mapToGlobal(QPoint(0, 0))
        VolumeBtnrect = QRect(p, self.VolumeBtn.geometry().size())
        if(not VolumeBtnrect.contains(QtGui.QCursor().pos())):
            self.VolumeBtn.setChecked(False)
        QtWidgets.QDialog.closeEvent(self.VolumeSliderWrapper, e)

    def PlayMedia(self, FilePath: str):
        if(not Path(FilePath).is_file()):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Error: Could not find file")
            msg.setInformativeText('The specified file could not be opened')
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        
        if(FilePath.endswith(".mp4")):
            self.player.play(FilePath)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MediaPlayerWidget = MediaPlayetrWidget()
    MediaPlayerWidget.setWindowTitle("MediaPlayer")
    MediaPlayerWidget.show()
    MediaPlayerWidget.PlayMedia(r"test_files\1.mp4")
    MediaPlayerWidget.player.volume = 30
    sys.exit(app.exec_())
