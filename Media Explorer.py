from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QUrl, QMimeData, QSize, QSettings, Qt
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent, QKeySequence
from src.builds.ui_mainwindow import Ui_MainWindow
from src.MediaPlayerWidget import MediaPlayerWidget
from pathlib import Path
import os
from src.QuickActionBtn import QuickActionBtn
import bisect


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.app = app
        super().__init__()
        self.setupUi(self)

        self.settings = QSettings()
        LastUsedPath = self.settings.value(
            "init/LastUsedPath", os.path.expandvars(r"C:\Users\%USERNAME%\Desktop"))

        self.MediaPlayerWidget = MediaPlayerWidget(self.MediaPlayerContainer)
        self.MediaPlayerContainerLayout.addWidget(self.MediaPlayerWidget)
        self.FileOpenDialog = QFileDialog(self)
        self.FileOpenDialog.setFileMode(QFileDialog.ExistingFile)
        self.FolderOpenDialog = QFileDialog(self)
        self.FolderOpenDialog.setFileMode(QFileDialog.Directory)
        self.FolderOpenDialog.setOptions(
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.AddMoveActionDialog = QFileDialog(self)
        self.AddMoveActionDialog.setFileMode(QFileDialog.Directory)
        self.AddMoveActionDialog.setOptions(
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.AddCopyActionDialog = QFileDialog(self)
        self.AddCopyActionDialog.setFileMode(QFileDialog.Directory)
        self.AddCopyActionDialog.setOptions(
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.AddSubdirMoveActionDialog = QFileDialog(self)
        self.AddSubdirMoveActionDialog.setFileMode(QFileDialog.Directory)
        self.AddSubdirMoveActionDialog.setOptions(
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.SetFileInitDirs(LastUsedPath)
        self.ActionBtnGroup = QtWidgets.QButtonGroup(self)
        self.DeleteBtn = QuickActionBtn(self.DefaultActions)
        self.DeleteBtn.setMinimumSize(QSize(32, 32))
        self.DeleteBtn.setMaximumSize(QSize(32, 32))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/assets/delete.svg"),
                       QIcon.Normal, QIcon.Off)
        self.DeleteBtn.setIcon(icon)
        self.DeleteBtn.setIconSize(QSize(24, 24))
        self.DeleteBtn.setToolTip(
            "<html><head/><body><p>Delete File<br/>shortcut:&lt;del&gt;</p></body></html>")
        self.DefaultActionsLayout.addWidget(self.DeleteBtn)
        self.ActionBtnGroup.addButton(self.DeleteBtn)
        self.ActionRemoveMenuGroup = QtWidgets.QActionGroup(self)

        self.CurrFileIdx = -1
        self.FileList = []
        self.PrevTasksList = []

        self.MediaPlayerWidget.dropOpen.connect(
            lambda f: self.OpenFile(f, True))
        self.PrevFileBtn.clicked.connect(self.PrevFile)
        self.NextFileBtn.clicked.connect(self.NextFile)
        self.CopyToClipBtn.clicked.connect(self.CopyToClip)
        self.actionOpen_File.triggered.connect(self.FileOpenDialog.open)
        self.actionOpen_Folder.triggered.connect(self.FolderOpenDialog.open)
        self.actionAdd_move_action.triggered.connect(
            self.AddMoveActionDialog.open)
        self.actionAdd_copy_action.triggered.connect(
            self.AddCopyActionDialog.open)
        self.actionRemove_all_actions.triggered.connect(
            self.DeleteAllActionBtn)
        self.actionAdd_subdir_move_action.triggered.connect(
            self.AddSubdirMoveActionDialog.open)
        self.FileOpenDialog.fileSelected.connect(self.OpenFile)
        self.FolderOpenDialog.fileSelected.connect(self.OpenFolder)
        self.AddMoveActionDialog.fileSelected.connect(self.AddCustomMoveAction)
        self.AddCopyActionDialog.fileSelected.connect(self.AddCustomCopyAction)
        self.AddSubdirMoveActionDialog.fileSelected.connect(
            self.AddCustomSubdirMoveActions)
        self.ActionBtnGroup.buttonClicked.connect(self.ActionBtnClicked)
        self.ActionRemoveMenuGroup.triggered.connect(self.DeleteActionBtn)
        self.UndoActionBtn.clicked.connect(self.UndoPrevAction)

    def SetFileInitDirs(self, LastUsedPath):
        self.FileOpenDialog.setDirectory(LastUsedPath)
        self.FolderOpenDialog.setDirectory(LastUsedPath)
        self.AddMoveActionDialog.setDirectory(LastUsedPath)
        self.AddCopyActionDialog.setDirectory(LastUsedPath)
        self.AddSubdirMoveActionDialog.setDirectory(LastUsedPath)

        self.settings.setValue("init/LastUsedPath", LastUsedPath)

    def initFileList(self, Dir):
        self.FileList = []
        for p in Path(Dir).resolve().iterdir():
            if p.is_file():
                bisect.insort(self.FileList, str(
                    p), key=lambda e: -1*os.path.getmtime(e))

    def keyPressEvent(self, e: QKeyEvent):
        if(e.key() == Qt.Key.Key_Space):
            self.MediaPlayerWidget.VideoPlayer.TogglePause()
        elif(e.key() == Qt.Key.Key_Right):
            self.NextFile()
        elif(e.key() == Qt.Key.Key_Left):
            self.PrevFile()
        elif(e.matches(QKeySequence.StandardKey.Copy)):
            self.CopyToClip()
        elif(e.matches(QKeySequence.StandardKey.Undo)):
            self.UndoPrevAction()

    def OpenFolder(self, Dir):
        if(not Path(Dir).is_dir()):
            print("Invalid directory")
            return
        self.initFileList(Dir)
        self.MediaPlayerWidget.OpenFile(self.FileList[0])
        self.CurrFileIdx = 0
        self.SetFileInitDirs(Dir)

    def OpenFile(self, FilePath, isDropOpen=False):
        path = Path(FilePath).resolve()
        if(not path.is_file()):
            print("Invalid file path")
            return
        self.initFileList(path.parent)
        self.CurrFileIdx = self.FileList.index(str(path))
        if(not isDropOpen):
            self.MediaPlayerWidget.OpenFile(str(path))
        self.SetFileInitDirs(str(path.parent))

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

    def AddCustomBtn(self, DestDir, type):
        path = Path(DestDir).resolve()
        if(not path.is_dir()):
            print("Path is not a directory")
            return
        elif(type not in {"move", "copy"}):
            print('type must be "move" or "copy"')
        NewBtn = QuickActionBtn(self.CustomActions, path.name, type, str(path))
        NewBtn.setToolTip(
            f"<html><head/><body><p>{type} current file to {DestDir}</p></body></html>")
        self.CustomActionsLayout.addWidget(NewBtn)
        NewBtn.setObjectName(type+"btn")
        self.ActionBtnGroup.addButton(NewBtn)
        NewQAction = QtWidgets.QAction(self)
        NewQAction.ActionBtn = NewBtn
        NewQAction.setText(path.name)
        self.menuRemove_Actions.addAction(NewQAction)
        self.ActionRemoveMenuGroup.addAction(NewQAction)

    def AddCustomMoveAction(self, DestDir):
        self.AddCustomBtn(DestDir, "move")
        self.SetFileInitDirs(DestDir)

    def AddCustomCopyAction(self, DestDir):
        self.AddCustomBtn(DestDir, "copy")
        self.SetFileInitDirs(DestDir)

    def AddCustomSubdirMoveActions(self, DestDir):
        path = Path(DestDir).resolve()
        for i in path.iterdir():
            if(i.is_dir()):
                self.AddCustomMoveAction(str(i))
        self.SetFileInitDirs(DestDir)

    def DeleteActionBtn(self, btn: QtWidgets.QAction):
        btn.ActionBtn.deleteLater()
        btn.deleteLater()

    def DeleteAllActionBtn(self):
        for i in self.ActionRemoveMenuGroup.actions():
            self.DeleteActionBtn(i)

    def ActionBtnClicked(self, btn: QuickActionBtn):
        if(self.CurrFileIdx == -1):
            return
        # file is no longer at path
        if(not btn.ExecuteTask(self.FileList[self.CurrFileIdx])):
            del self.FileList[self.CurrFileIdx]
            self.CurrFileIdx -= 1
            self.NextFile()
        self.PrevTasksList.append(btn)

    def UndoPrevAction(self):
        if(len(self.PrevTasksList) == 0):
            return
        FilePath = self.PrevTasksList[-1].UnExecuteTask()
        def key(e): return -1*os.path.getmtime(e)
        self.CurrFileIdx = bisect.bisect(self.FileList, key(FilePath),
                                         key=key)
        self.FileList.insert(self.CurrFileIdx, FilePath)
        self.MediaPlayerWidget.OpenFile(self.FileList[self.CurrFileIdx])
        self.PrevTasksList.pop()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("FieryRMS")
    app.setOrganizationDomain("https://github.com/FieryRMS/File-Sorter")
    app.setApplicationName("File Sorter")
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
