import sys
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from pathlib import Path

IMAGEPDFVIEWER = Path(__file__).parent.joinpath(
    "imagepdfviewer/index.html").resolve().as_uri()


class ImagePdfViewerWidget(QWebEngineView):
    IMAGETYPES = (".png", ".jpg", ".jpeg", ".webp", "svg",
                  ".apng", ".avif", ".jfif", ".pjpeg", ".pjp")

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setAcceptDrops(False)
        self.load(QUrl(IMAGEPDFVIEWER))
        self.DevWindow()

    def OpenPdf(self, uri):
        self.page().runJavaScript(f"OpenPdf('{uri}')")

    def OpenImage(self, uri):
        self.page().runJavaScript(f"OpenImage('{uri}')")

    def HideAll(self):
        self.page().runJavaScript("HideAll()")

    def OpenFile(self, FilePath: str):
        if(not Path(FilePath).is_file()):
            print("file not found")
            return

        if(FilePath.endswith(".pdf")):
            self.OpenPdf(Path(FilePath).resolve().as_uri())
        elif(FilePath.endswith(self.IMAGETYPES)):
            self.OpenImage(Path(FilePath).resolve().as_uri())
        else:
            print("unknown file format")

    def DevWindow(self):
        self.dev_view = QWebEngineView()
        self.page().setDevToolsPage(self.dev_view.page())
        self.dev_view.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ImagePdfViewerWidget()
    window.setGeometry(200, 50, 800, 600)
    window.OpenFile(r"test_files\6.webp")
    window.show()
    # window.DevWindow()
    sys.exit(app.exec_())
