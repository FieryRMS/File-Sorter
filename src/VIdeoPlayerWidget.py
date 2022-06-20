if(1):  # prevent formatter from formatting this
    import os
    os.environ['PATH'] += os.pathsep + os.path.abspath(
        'dlls/')
from pathlib import Path
from ui_videoplayerwidget import Ui_VideoPlayerWidget
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QPoint, QRect
from PyQt5 import QtWidgets, QtGui
import mpv
from numpy import interp


class VideoPlayetrWidget(QtWidgets.QWidget, Ui_VideoPlayerWidget):
    percentpos = pyqtSignal(float, name="percentpos")

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # Attach video output to VideoContainer
        self.VideoContainer.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.VideoContainer.setAttribute(Qt.WA_NativeWindow)
        self.player = mpv.MPV(
            wid=str(int(self.VideoContainer.winId()))
        )
        self.UnPause(False)
        self.player.loop_playlist = 'inf'

        # Make the slider into a popup, slider doesnt render when mpv is attached
        self.verticalLayout.removeWidget(self.VolumeSlider)
        self.VolumeSliderWrapper = QtWidgets.QDialog()
        self.VolumeSlider.setParent(self.VolumeSliderWrapper)
        self.VolumeSliderWrapper.setStyleSheet("background: transparent")
        self.VolumeSliderWrapper.setWindowFlags(
            Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Popup)
        self.VolumeSliderWrapper.setAttribute(Qt.WA_TranslucentBackground)

        self.VolumeBtn.clicked['bool'].connect(self.ShowVolumeSlider)
        self.VolumeSliderWrapper.closeEvent = self.UnselectVolumeBtnOnVolSliderClose
        self.VolumeSlider.valueChanged['int'].connect(
            self.SetVolumeFromSliderValue)

        self.PlayPauseBtn.clicked['bool'].connect(self.UnPause)

        self.TimelineSlider.valueChanged['int'].connect(self.SetTime)
        self.TimelineSlider.mousePressEvent = self.SetisSeeking
        self.TimelineSlider.mouseReleaseEvent = self.UnsetisSeeking
        self.TimelineSlider.mouseMoveEvent = self.TimeLineMoveToClickPos
        self.isSeeking = False
        self.wasPlaying = False

        self.VideoContainer.mouseReleaseEvent = self.VideoContClickUnPause

        @self.player.property_observer('percent-pos')
        def time_observer(_, percentage):
            if(percentage and not self.isSeeking):
                value = interp(percentage, [0, 100], [
                               self.TimelineSlider.minimum(), self.TimelineSlider.maximum()])
                self.TimelineSlider.setValue(int(value))

        @self.player.event_callback("end-file")
        def endfile_observer(e):
            self.TimelineSlider.setValue(0)
            self.UnPause(False)

    @pyqtSlot(bool)
    def UnPause(self, playing):
        self.PlayPauseBtn.setChecked(playing)
        self.player.pause = not playing

    @pyqtSlot(bool)
    def TogglePause(self):
        self.UnPause(self.player.pause)

    @pyqtSlot(bool)
    def ShowVolumeSlider(self, checked):
        self.VolumeSliderWrapper.setVisible(checked)
        if(checked):
            p = self.VolumeBtn.mapToGlobal(QPoint(3, -130))
            self.VolumeSliderWrapper.move(p)

    @pyqtSlot(int)
    def SetVolumeFromSliderValue(self, val):
        if not hasattr(self.VolumeSlider, "prevPercentage"):
            self.VolumeSlider.prevPercentage = 100
        self.VolumeSlider.setValue(int(val))
        percentage = interp(val, [self.VolumeSlider.minimum(),
                                  self.VolumeSlider.maximum()], [0, 100])

        self.player.volume = percentage
        limits = [5, 35, 75]
        if(percentage >= limits[2] and self.VolumeSlider.prevPercentage < limits[2]):
            icon = QtGui.QIcon(":/icons/assets/volume-high.svg")
            self.VolumeBtn.setIcon(icon)
        elif((percentage < limits[2] and self.VolumeSlider.prevPercentage >= limits[2])
                or (percentage >= limits[1] and self.VolumeSlider.prevPercentage < limits[1])):
            icon = QtGui.QIcon(":/icons/assets/volume-medium.svg")
            self.VolumeBtn.setIcon(icon)
        elif((percentage < limits[1] and self.VolumeSlider.prevPercentage >= limits[1])
                or (percentage >= limits[0] and self.VolumeSlider.prevPercentage < limits[0])):
            icon = QtGui.QIcon(":/icons/assets/volume-low.svg")
            self.VolumeBtn.setIcon(icon)
        elif(percentage < limits[0] and self.VolumeSlider.prevPercentage >= limits[0]):
            icon = QtGui.QIcon(":/icons/assets/volume-off.svg")
            self.VolumeBtn.setIcon(icon)

        self.VolumeSlider.prevPercentage = percentage

    @pyqtSlot(int)
    def SetTime(self, val):
        if(self.isSeeking):
            self.TimelineSlider.setValue(int(val))
            percentage = interp(val, [self.TimelineSlider.minimum(),
                                      self.TimelineSlider.maximum()], [0, 100])
            if(self.player.duration):
                time = percentage*self.player.duration/100
                self.player.seek(time, "absolute+exact")

    def SetisSeeking(self, e):
        if e.button() == Qt.LeftButton:
            self.isSeeking = True
            self.wasPlaying = not self.player.pause
            self.UnPause(False)
            e.accept()
            x = e.pos().x()
            self.SetTime(int(self.GetTimeLineValFromClickX(x)))
        else:
            QtWidgets.QSlider.mousePressEvent(self.TimelineSlider, e)

    def UnsetisSeeking(self, e):
        if e.button() == Qt.LeftButton:
            self.isSeeking = False
            self.UnPause(self.wasPlaying)
            e.accept()
            x = e.pos().x()
            self.SetTime(int(self.GetTimeLineValFromClickX(x)))
        else:
            QtWidgets.QSlider.mousePressEvent(self.TimelineSlider, e)

    def TimeLineMoveToClickPos(self, e):
        x = e.pos().x()
        self.SetTime(int(self.GetTimeLineValFromClickX(x)))
        QtWidgets.QSlider.mousePressEvent(self.TimelineSlider, e)

    def GetTimeLineValFromClickX(self, x):
        btnwidth = 10

        # centering button to mouse click
        if(x < btnwidth/2):
            x = btnwidth/2
        elif(x > self.TimelineSlider.width()-btnwidth/2):
            x = self.TimelineSlider.width()-btnwidth/2
        x -= btnwidth/2
        ratio = x / (self.TimelineSlider.width()-btnwidth)

        value = (self.TimelineSlider.maximum() - self.TimelineSlider.minimum()) * \
            ratio + self.TimelineSlider.minimum()
        return value

    def UnselectVolumeBtnOnVolSliderClose(self, e):
        # prevent double click on volume button
        p = self.VolumeBtn.mapToGlobal(QPoint(0, 0))
        VolumeBtnrect = QRect(p, self.VolumeBtn.geometry().size())
        if(not VolumeBtnrect.contains(QtGui.QCursor().pos())):
            self.VolumeBtn.setChecked(False)

        QtWidgets.QDialog.closeEvent(self.VolumeSliderWrapper, e)

    def VideoContClickUnPause(self, e):
        if e.button() == Qt.LeftButton:
            self.TogglePause()
        else:
            QtWidgets.QWidget.mousePressEvent(self.VideoContainer, e)

    def SetVolumeFromPercentage(self, percentage):
        if(percentage<0):
            percentage=0
        elif(percentage>100):
            percentage=100
        value = interp(percentage, [0, 100], [
            self.VolumeSlider.minimum(), self.VolumeSlider.maximum()])
        self.SetVolumeFromSliderValue(value)

    def PlayVideo(self, FilePath: str):
        if(not Path(FilePath).is_file()):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Error: Could not find file")
            msg.setInformativeText('The specified file could not be opened')
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        # if(FilePath.endswith(".mp4")):
        self.player.play(FilePath)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VideoPlayerWidget = VideoPlayetrWidget()
    VideoPlayerWidget.setWindowTitle("VideoPlayer")
    VideoPlayerWidget.show()
    VideoPlayerWidget.PlayVideo(r"test_files\1.mp4")
    VideoPlayerWidget.SetVolumeFromPercentage(30)
    sys.exit(app.exec_())
