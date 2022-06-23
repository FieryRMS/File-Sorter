from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QUrl, QMimeData
from src.builds.ui_mainwindow import Ui_MainWindow
from src.MediaPlayerWidget import MediaPlayerWidget
from pathlib import Path
import shutil
import os
from send2trash import send2trash


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.app = app
        super().__init__()
        self.setupUi(self)

        self.MediaPlayerWidget = MediaPlayerWidget(self.MediaPlayerContainer)
        self.MediaPlayerContainerLayout.addWidget(self.MediaPlayerWidget)
        self.FileOpenDialog = QFileDialog(self)
        self.FileOpenDialog.setFileMode(QFileDialog.ExistingFile)
        self.FolderOpenDialog = QFileDialog(self)
        self.FolderOpenDialog.setFileMode(QFileDialog.Directory)
        self.FolderOpenDialog.setOptions(QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.CurrFileIdx = -1
        self.FileList = []

        self.MediaPlayerWidget.dropOpen.connect(self.OpenFile)
        self.PrevFileBtn.clicked.connect(self.PrevFile)
        self.NextFileBtn.clicked.connect(self.NextFile)
        self.DeleteBtn.clicked.connect(self.Delete)
        self.CopyToClipBtn.clicked.connect(self.CopyToClip)
        self.actionOpen_File.triggered.connect(self.FileOpenDialog.open)
        self.actionOpen_Folder.triggered.connect(self.FolderOpenDialog.open)
        self.FileOpenDialog.fileSelected.connect(self.OpenFile)
        self.FolderOpenDialog.fileSelected.connect(self.OpenFolder)

    def initFileList(self, Dir):
        self.FileList = [str(p) for p in Path(
            Dir).resolve().iterdir() if p.is_file()]
        self.FileList.sort(key=lambda e: os.path.getmtime(e))

    def OpenFolder(self, Dir):
        if(not Path(Dir).is_dir()):
            print("Invalid directory")
            return
        self.initFileList(Dir)
        self.MediaPlayerWidget.OpenFile(self.FileList[0])
        self.CurrFileIdx = 0

    def OpenFile(self, FilePath, isDropOpen=False):
        path = Path(FilePath).resolve()
        if(not path.is_file()):
            print("Invalid file path")
            return
        self.initFileList(path.parent)
        path = str(path)
        self.CurrFileIdx = self.FileList.index(path)
        if(not isDropOpen):
            self.MediaPlayerWidget.OpenFile(path)

    def NextFile(self):
        if(len(self.FileList) == 0):
            return
        self.CurrFileIdx += 1
        if(self.CurrFileIdx >= len(self.FileList)):
            self.CurrFileIdx = 0
        self.MediaPlayerWidget.OpenFile(self.FileList[self.CurrFileIdx])

    def PrevFile(self):
        if(len(self.FileList) == 0):
            return
        self.CurrFileIdx -= 1
        if(self.CurrFileIdx < 0):
            self.CurrFileIdx = len(self.FileList)-1
        self.MediaPlayerWidget.OpenFile(self.FileList[self.CurrFileIdx])

    def CopyToClip(self):
        if(self.CurrFileIdx == -1):
            return
        FilePath = self.FileList[self.CurrFileIdx]
        if(not Path(FilePath).is_file()):
            print("Invalid file path")
            return

        data = QMimeData()
        data.setUrls([QUrl.fromLocalFile(FilePath)])
        barr = bytearray()
        barr.extend(map(ord, FilePath+"\x00"))
        data.setData('application/x-qt-windows-mime;value="FileName"', barr)
        cb = QtWidgets.QApplication.clipboard()
        cb.setMimeData(data)

    def Delete(self):
        if(self.CurrFileIdx == -1):
            return
        FilePath = self.FileList[self.CurrFileIdx]
        if(not Path(FilePath).is_file()):
            print("Invalid file path")
            return
        send2trash(FilePath)


class QuickActionBtn(QtWidgets.QPushButton):
    def __init__(self, name, parent=None, type="delete", destdir=None):
        if(type not in {"move", "delete", "copy"}):
            raise ValueError(
                'In QuickActionBtn.__init__(): type must be "move", "delete" or "copy"')

        if(type != "delete" and not Path(destdir).is_dir()):
            raise ValueError(
                'In QuickActionBtn.__init__(): type "move", "copy" must have valid destdir')

        super().__init__(parent)
        self.DestDir = destdir

        if(type == "move"):
            self.Task = self.Move
        if(type == "delete"):
            self.Task = self.Delete
        if(type == "copy"):
            self.Task = self.Copy

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setText(name)

        self.TaskList = []
        self.prevTasks = []

    def Copy(self):
        FailedList = []
        SuccessList = []
        for file in self.TaskList:
            path = Path(file)
            CurrLoc = str(path.absolute())
            try:
                shutil.copy2(CurrLoc, self.DestDir)
                SuccessList.append(CurrLoc)
            except:
                FailedList.append(CurrLoc)
        return SuccessList, FailedList

    def Move(self):
        FailedList = []
        SuccessList = []
        for file in self.TaskList:
            CurrLoc = str(Path(file).absolute())
            try:
                shutil.move(CurrLoc, self.DestDir)
                SuccessList.append(CurrLoc)
            except:
                FailedList.append(CurrLoc)
        return SuccessList, FailedList

    def Delete(self):
        FailedList = []
        SuccessList = []
        for file in self.TaskList:
            CurrLoc = str(Path(file).absolute())
            try:
                send2trash(CurrLoc)
                SuccessList.append(CurrLoc)
            except:
                FailedList.append(CurrLoc)
        return SuccessList, FailedList

    def AddToTaskList(self, file):
        self.TaskList.append(file)

    def ExecuteTask(self):
        SuccessList, FailedList = self.Task()
        self.TaskList = []
        self.prevTasks.append(SuccessList)
        print("failed tasks:")
        print(FailedList)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
