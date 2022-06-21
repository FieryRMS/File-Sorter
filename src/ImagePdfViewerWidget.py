import sys
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from pathlib import Path

PDFJS = Path(__file__).parent.joinpath("pdfjs/index.html").resolve().as_uri()
IVVIEWER = Path(__file__).parent.joinpath(
    "iv-viewer/index.html").resolve().as_uri()


class ImagePdfViewerWidget(QWebEngineView):
    IMAGETYPES = (".png", ".jpg", ".jpeg", ".webp", "svg",
                  ".apng", ".avif", ".jfif", ".pjpeg", ".pjp")

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setHtml(r"<style>*{background:#0d0d0d;}</style>")
        self.setContextMenuPolicy(Qt.NoContextMenu)
        
        self.isPdf = False
        self.isImage = False

    def LoadPdf(self, uri):
        if(self.isPdf):
            self.page().runJavaScript('PDFViewerApplication.open({})'.format(uri))
        else:
            self.load(QUrl(PDFJS+"?file={}".format(uri)))
            self.isPdf = True
            self.isImage = False

    def LoadImage(self, uri):
        if(self.isPdf):
            self.page().runJavaScript('OpenImage({})'.format(uri))
        else:
            self.load(QUrl(IVVIEWER+"?file={}".format(uri)))
            self.isPdf = False
            self.isImage = True

    def LoadFile(self, path: str):
        if(not Path(path).is_file()):
            print("file not found")
            return

        if(path.endswith(".pdf")):
            self.LoadPdf(Path(path).resolve().as_uri())
        elif(path.endswith(self.IMAGETYPES)):
            self.LoadImage(Path(path).resolve().as_uri())
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
    window.LoadFile(r"test_files\6.webp")
    window.show()
    # window.DevWindow()
    sys.exit(app.exec_())
