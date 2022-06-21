from VideoPlayerWidget import VideoPlayerWidget
from ImagePdfViewerWidget import ImagePdfViewerWidget

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class MediaPlayerWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.VideoPlayer = VideoPlayerWidget(self)
        self.ImagePdfViewer = ImagePdfViewerWidget(self)

        self.UnknownFile = QtWidgets.QLabel(self)
        self.UnknownFile.setAlignment(Qt.AlignCenter)
        self.UnknownFile.setText("OMGOMGOMOMGGGGG")

        self.StackedLayout = QtWidgets.QStackedLayout(self)
        self.StackedLayout.addWidget(self.VideoPlayer)
        self.StackedLayout.addWidget(self.ImagePdfViewer)
        self.StackedLayout.addWidget(self.UnknownFile)

        self.StackedLayout.setCurrentWidget(self.UnknownFile)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MediaPlayerWidget()
    ui.show()
    sys.exit(app.exec_())
