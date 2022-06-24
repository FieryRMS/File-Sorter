from .VideoPlayerWidget import VideoPlayerWidget
from .ImagePdfViewerWidget import ImagePdfViewerWidget

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from pathlib import Path
from win32com.client.gencache import EnsureDispatch


class MediaPlayerWidget(QtWidgets.QWidget):
    dropOpen = pyqtSignal(str, name="dropOpen")

    UnknownFileText = """
<table align="center" cellpadding="4px" style="font-size:15px;border-collapse: collapse;">
    <tbody>
        <tr>
            <td style="border-bottom: 1px solid white">Unsupported file format:</td>
            <td style="border-bottom: 1px solid white"></td>
        </tr>
        <tr>
            <td style="border-bottom: 1px solid white">Name:</td>
            <td style="border-bottom: 1px solid white">{NAME}</td>
        </tr>
        <tr>
            <td style="border-bottom: 1px solid white">Size:</td>
            <td style="border-bottom: 1px solid white">{SIZE}</td>
        </tr>
        <tr>
            <td style="border-bottom: 1px solid white">Item type:</td>
            <td style="border-bottom: 1px solid white">{TYPE}</td>
        </tr>
        <tr>
            <td style="border-bottom: 1px solid white">Date created:</td>
            <td style="border-bottom: 1px solid white">{DATEC}</td>
        </tr>
        <tr>
            <td style="border-bottom: 1px solid white">Date modified:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
            <td style="border-bottom: 1px solid white">{DATEM}</td>
        </tr>
    </tbody>
</table>
"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.VideoPlayer = VideoPlayerWidget(self)
        self.ImagePdfViewer = ImagePdfViewerWidget(self)

        self.UnknownFile = QtWidgets.QLabel(self)
        self.UnknownFile.setAlignment(Qt.AlignCenter)
        self.UnknownFile.setTextFormat(Qt.TextFormat.RichText)
        self.UnknownFile.setStyleSheet(
            "QLabel { background: #0d0d0d; color: white; }")

        self.StackedLayout = QtWidgets.QStackedLayout(self)
        self.StackedLayout.addWidget(self.VideoPlayer)
        self.StackedLayout.addWidget(self.ImagePdfViewer)
        self.StackedLayout.addWidget(self.UnknownFile)

        self.UnknownFile.setText("""
        <p style="text-align:center"><span style="font-size:18px">Drop files to open...</span></p>
""")
        self.StackedLayout.setCurrentWidget(self.UnknownFile)

    def get_file_metadata(self, path, filename):
        # https://stackoverflow.com/a/63662404
        metadata = ['Name', 'Size', 'Item type',
                    'Date modified', 'Date created']
        sh = EnsureDispatch('Shell.Application', 0)
        ns = sh.NameSpace(path)

        file_metadata = dict()
        item = ns.ParseName(str(filename))
        for ind, attribute in enumerate(metadata):
            attr_value = ns.GetDetailsOf(item, ind)
            if attr_value:
                file_metadata[attribute] = attr_value

        return file_metadata

    def OpenFile(self, FilePath: str):
        if(not Path(FilePath).is_file()):
            print("file not found")
        elif(FilePath.endswith(self.VideoPlayer.VIDEOTYPES)):
            self.VideoPlayer.OpenVideo(FilePath)
            self.StackedLayout.setCurrentWidget(self.VideoPlayer)
        elif(FilePath.endswith(".pdf") or
             FilePath.endswith(self.ImagePdfViewer.IMAGETYPES)):
            self.ImagePdfViewer.OpenFile(FilePath)
            self.StackedLayout.setCurrentWidget(self.ImagePdfViewer)
        else:
            path = Path(FilePath).resolve()
            metadata = self.get_file_metadata(str(path.parent), str(path.name))
            self.UnknownFile.setText(self.UnknownFileText.format(
                NAME=metadata['Name'],
                SIZE=metadata['Size'],
                TYPE=metadata['Item type'],
                DATEC=metadata['Date modified'],
                DATEM=metadata['Date created']
            ))
            self.ImagePdfViewer.HideAll()
            self.StackedLayout.setCurrentWidget(self.UnknownFile)

    def dragEnterEvent(self, event):
        if(event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1
                and event.mimeData().urls()[0].isLocalFile()):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        f = event.mimeData().urls()[0].toLocalFile()
        self.OpenFile(f)
        self.dropOpen.emit(f)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MediaPlayerWidget()
    ui.resize(660, 480)
    # ui.OpenFile(r"test_files\1.mp4")
    ui.show()
    sys.exit(app.exec_())
