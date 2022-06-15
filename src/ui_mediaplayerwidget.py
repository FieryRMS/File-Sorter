# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\MediaPlayer.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MediaPlayerWidget(object):
    def setupUi(self, MediaPlayerWidget):
        MediaPlayerWidget.setObjectName("MediaPlayerWidget")
        MediaPlayerWidget.resize(718, 542)
        MediaPlayerWidget.setStyleSheet("background-color: rgb(29, 29, 29);")
        self.gridLayout = QtWidgets.QGridLayout(MediaPlayerWidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.VideoController = QtWidgets.QFrame(MediaPlayerWidget)
        self.VideoController.setMaximumSize(QtCore.QSize(16777215, 35))
        self.VideoController.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.VideoController.setFrameShadow(QtWidgets.QFrame.Raised)
        self.VideoController.setObjectName("VideoController")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.VideoController)
        self.horizontalLayout.setContentsMargins(0, 2, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.PlayPauseBtn = QtWidgets.QPushButton(self.VideoController)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlayPauseBtn.sizePolicy().hasHeightForWidth())
        self.PlayPauseBtn.setSizePolicy(sizePolicy)
        self.PlayPauseBtn.setMinimumSize(QtCore.QSize(32, 32))
        self.PlayPauseBtn.setMaximumSize(QtCore.QSize(32, 32))
        self.PlayPauseBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PlayPauseBtn.setStyleSheet("QPushButton {\n"
"    border: 2px solid black;\n"
"    border-radius: 16px;\n"
"    background: rgb(190, 190, 190)\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(180, 180, 180);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(160, 160, 160);\n"
"}")
        self.PlayPauseBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\../assets/play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("ui\\../assets/pause.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.PlayPauseBtn.setIcon(icon)
        self.PlayPauseBtn.setIconSize(QtCore.QSize(24, 24))
        self.PlayPauseBtn.setCheckable(True)
        self.PlayPauseBtn.setChecked(False)
        self.PlayPauseBtn.setObjectName("PlayPauseBtn")
        self.horizontalLayout.addWidget(self.PlayPauseBtn)
        self.PrevBtn = QtWidgets.QPushButton(self.VideoController)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrevBtn.sizePolicy().hasHeightForWidth())
        self.PrevBtn.setSizePolicy(sizePolicy)
        self.PrevBtn.setMinimumSize(QtCore.QSize(32, 32))
        self.PrevBtn.setMaximumSize(QtCore.QSize(32, 32))
        self.PrevBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PrevBtn.setStyleSheet("QPushButton {\n"
"    border: 2px solid black;\n"
"    border-radius: 16px;\n"
"    background: rgb(190, 190, 190)\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(180, 180, 180);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(160, 160, 160);\n"
"}")
        self.PrevBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ui\\../assets/skip-previous.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PrevBtn.setIcon(icon1)
        self.PrevBtn.setIconSize(QtCore.QSize(24, 24))
        self.PrevBtn.setCheckable(False)
        self.PrevBtn.setChecked(False)
        self.PrevBtn.setObjectName("PrevBtn")
        self.horizontalLayout.addWidget(self.PrevBtn)
        self.NextBtn = QtWidgets.QPushButton(self.VideoController)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NextBtn.sizePolicy().hasHeightForWidth())
        self.NextBtn.setSizePolicy(sizePolicy)
        self.NextBtn.setMinimumSize(QtCore.QSize(32, 32))
        self.NextBtn.setMaximumSize(QtCore.QSize(32, 32))
        self.NextBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.NextBtn.setStyleSheet("QPushButton {\n"
"    border: 2px solid black;\n"
"    border-radius: 16px;\n"
"    background: rgb(190, 190, 190)\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(180, 180, 180);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(160, 160, 160);\n"
"}")
        self.NextBtn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ui\\../assets/skip-next.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.NextBtn.setIcon(icon2)
        self.NextBtn.setIconSize(QtCore.QSize(24, 24))
        self.NextBtn.setCheckable(False)
        self.NextBtn.setChecked(False)
        self.NextBtn.setObjectName("NextBtn")
        self.horizontalLayout.addWidget(self.NextBtn)
        self.TimelineSlider = QtWidgets.QSlider(self.VideoController)
        self.TimelineSlider.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.TimelineSlider.setStyleSheet("QSlider::groove { \n"
"    background-color: white;\n"
"    height: 4px;\n"
"}\n"
"\n"
"QSlider::handle { \n"
"    background-color: rgb(190, 190, 190); \n"
"    width: 10px;\n"
"    margin: -8px, -8px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QSlider::handle:hover {\n"
"    background-color: rgb(180, 180, 180);\n"
"}\n"
"\n"
"QSlider::handle:pressed {\n"
"    background-color: rgb(160, 160, 160);\n"
"}")
        self.TimelineSlider.setMaximum(10000)
        self.TimelineSlider.setPageStep(100)
        self.TimelineSlider.setOrientation(QtCore.Qt.Horizontal)
        self.TimelineSlider.setInvertedAppearance(False)
        self.TimelineSlider.setInvertedControls(False)
        self.TimelineSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.TimelineSlider.setObjectName("TimelineSlider")
        self.horizontalLayout.addWidget(self.TimelineSlider)
        self.Volume = QtWidgets.QToolButton(self.VideoController)
        self.Volume.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Volume.setStyleSheet("QToolButton {\n"
"    border: 2px solid black;\n"
"    border-radius: 16px;\n"
"    background: rgb(190, 190, 190)\n"
"    }\n"
"\n"
"QToolButton:hover {\n"
"    background-color: rgb(180, 180, 180);\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    background-color: rgb(160, 160, 160);\n"
"}")
        self.Volume.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ui\\../assets/volume-high.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Volume.setIcon(icon3)
        self.Volume.setIconSize(QtCore.QSize(20, 20))
        self.Volume.setCheckable(True)
        self.Volume.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.Volume.setAutoRaise(False)
        self.Volume.setArrowType(QtCore.Qt.NoArrow)
        self.Volume.setObjectName("Volume")
        self.horizontalLayout.addWidget(self.Volume)
        self.gridLayout.addWidget(self.VideoController, 2, 0, 1, 1)
        self.MediaContainer = QtWidgets.QWidget(MediaPlayerWidget)
        self.MediaContainer.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.MediaContainer.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.MediaContainer.setObjectName("MediaContainer")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.MediaContainer)
        self.verticalLayout.setContentsMargins(5, -1, 3, 5)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.VolumeSlider = QtWidgets.QSlider(self.MediaContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VolumeSlider.sizePolicy().hasHeightForWidth())
        self.VolumeSlider.setSizePolicy(sizePolicy)
        self.VolumeSlider.setMinimumSize(QtCore.QSize(0, 120))
        self.VolumeSlider.setMaximumSize(QtCore.QSize(16777215, 150))
        self.VolumeSlider.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.VolumeSlider.setStyleSheet("QSlider::groove { \n"
"    background-color: white;\n"
"    width: 4px;\n"
"}\n"
"\n"
"QSlider::handle { \n"
"    background-color: rgb(190, 190, 190); \n"
"    height: 10px;\n"
"    margin: 0 -8px 0;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QSlider::handle:hover {\n"
"    background-color: rgb(180, 180, 180);\n"
"}\n"
"\n"
"QSlider::handle:pressed {\n"
"    background-color: rgb(160, 160, 160);\n"
"}")
        self.VolumeSlider.setMaximum(1000)
        self.VolumeSlider.setPageStep(100)
        self.VolumeSlider.setProperty("value", 1000)
        self.VolumeSlider.setOrientation(QtCore.Qt.Vertical)
        self.VolumeSlider.setObjectName("VolumeSlider")
        self.verticalLayout.addWidget(self.VolumeSlider)
        self.gridLayout.addWidget(self.MediaContainer, 0, 0, 1, 1)

        self.retranslateUi(MediaPlayerWidget)
        self.Volume.clicked['bool'].connect(self.VolumeSlider.setVisible) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MediaPlayerWidget)
        MediaPlayerWidget.setTabOrder(self.PlayPauseBtn, self.PrevBtn)
        MediaPlayerWidget.setTabOrder(self.PrevBtn, self.NextBtn)
        MediaPlayerWidget.setTabOrder(self.NextBtn, self.TimelineSlider)
        MediaPlayerWidget.setTabOrder(self.TimelineSlider, self.Volume)

    def retranslateUi(self, MediaPlayerWidget):
        _translate = QtCore.QCoreApplication.translate
        MediaPlayerWidget.setWindowTitle(_translate("MediaPlayerWidget", "Form"))
        self.PlayPauseBtn.setToolTip(_translate("MediaPlayerWidget", "<html><head/><body><p>Play/Pause<br/>shortcut: &lt;spacebar&gt;</p></body></html>"))
        self.PrevBtn.setToolTip(_translate("MediaPlayerWidget", "<html><head/><body><p>Previous<br/>shortcut: &lt;Left Arrow&gt;</p></body></html>"))
        self.NextBtn.setToolTip(_translate("MediaPlayerWidget", "<html><head/><body><p>Next<br/>shortcut: &lt;Right Arrow&gt;</p></body></html>"))
        self.TimelineSlider.setToolTip(_translate("MediaPlayerWidget", "<html><head/><body><p>seek</p></body></html>"))
        self.Volume.setToolTip(_translate("MediaPlayerWidget", "<html><head/><body><p>Volume</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MediaPlayerWidget = QtWidgets.QWidget()
    ui = Ui_MediaPlayerWidget()
    ui.setupUi(MediaPlayerWidget)
    MediaPlayerWidget.show()
    sys.exit(app.exec_())
