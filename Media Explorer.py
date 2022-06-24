from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QUrl, QMimeData, QSize, Qt
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from src.builds.ui_mainwindow import Ui_MainWindow
from src.MediaPlayerWidget import MediaPlayerWidget
from pathlib import Path
import shutil
import os
import send2trash
import winshell


class QuickActionBtn(QtWidgets.QPushButton):
    def __init__(self, parent=None, name=None, type="delete", destdir=None):
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
            self.UnTask = self.UnMove
        if(type == "delete"):
            self.Task = self.Delete
            self.UnTask = self.UnDelete
        if(type == "copy"):
            self.Task = self.Copy
            self.UnTask = self.UnCopy

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setText(name)

        self.prevTasksList = []

    def Copy(self, FilePath):
        try:
            shutil.copy2(FilePath, self.DestDir)
            return True
        except shutil.SameFileError:
            print("Error: src and dst specify the same file")
        except PermissionError:
            print("Error: The destination location is not writeable")
        except:
            print("Error: An unknown error occured")
        print(f"could not copy {FilePath} to {self.DestDir}")
        return False

    def Move(self, FilePath):
        try:
            shutil.move(FilePath, self.DestDir)
            return True
        except:
            print("Error: An unknown error occured")
        print(f"could not move {FilePath} to {self.DestDir}")
        return False

    def Delete(self, FilePath):
        try:
            send2trash.send2trash(FilePath)
            return True
        except FileNotFoundError:
            print("Error: File not found")
        except:
            print("Error: An unknown error occured")
        print(f"could not delete {FilePath}")
        return False

    ##returns true if file is still present in original dir
    def ExecuteTask(self, FilePath):
        FilePath = str(Path(FilePath).resolve())
        if(self.Task(FilePath)):
            self.prevTasksList.append(FilePath)
            if(self.Task==self.Copy):
                return True
            return False
        else:  # handle errors
            pass
        return True

    def UnCopy(self, FilePath):
        DestFile = Path(self.DestDir).join(Path(FilePath).name)
        return self.Delete(str(DestFile))

    def UnMove(self, FilePath):
        DestFile = Path(self.DestDir).join(Path(FilePath).name)
        try:
            shutil.move(DestFile, FilePath)
            return True
        except:
            print("Error: An unknown error occured")
        print(f"could not move {DestFile} to {FilePath}")
        return False

    def UnDelete(self, FilePath):
        try:
            winshell.undelete(FilePath)
            return True
        except ValueError:
            print("Error: File not found")
        except:
            print("Error: An unknown error occured")
        print(f"Could not restore {FilePath} from trash")
        return False

    def UnExecuteTask(self):
        if(len(self.prevTasksList) == 0):
            return

        if(self.UnTask(self.prevTasksList[-1])):
            self.prevTasksList.pop()
        else:  # handle errors
            pass


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
        self.FolderOpenDialog.setOptions(
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.ActionBtnGroup = QtWidgets.QButtonGroup(self.ActionHotbar)
        self.DeleteBtn = QuickActionBtn(self.DefaultActions)
        self.DeleteBtn.setMinimumSize(QSize(32, 32))
        self.DeleteBtn.setMaximumSize(QSize(32, 32))
        self.DeleteBtn.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/assets/delete.svg"),
                        QIcon.Normal, QIcon.Off)
        self.DeleteBtn.setIcon(icon)
        self.DeleteBtn.setIconSize(QSize(24, 24))
        self.DeleteBtn.setToolTip(
            "<html><head/><body><p>Delete File<br/>shortcut:&lt;del&gt;</p></body></html>")
        self.DefaultActionsLayout.addWidget(self.DeleteBtn)
        self.ActionBtnGroup.addButton(self.DeleteBtn)

        self.CurrFileIdx = -1
        self.FileList = []
        self.PrevTasksList=[]

        self.MediaPlayerWidget.dropOpen.connect(
            lambda f: self.OpenFile(f, True))
        self.PrevFileBtn.clicked.connect(self.PrevFile)
        self.NextFileBtn.clicked.connect(self.NextFile)
        self.CopyToClipBtn.clicked.connect(self.CopyToClip)
        self.actionOpen_File.triggered.connect(self.FileOpenDialog.open)
        self.actionOpen_Folder.triggered.connect(self.FolderOpenDialog.open)
        self.FileOpenDialog.fileSelected.connect(self.OpenFile)
        self.FolderOpenDialog.fileSelected.connect(self.OpenFolder)
        self.ActionBtnGroup.buttonClicked.connect(self.ActionBtnClicked)
        self.UndoActionBtn.clicked.connect(self.UndoPrevAction)

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

    def ActionBtnClicked(self, btn: QuickActionBtn):
        if(self.CurrFileIdx==-1):
            return
        btn.ExecuteTask(self.FileList[self.CurrFileIdx])
        self.PrevTasksList.append(btn)

    def UndoPrevAction(self):
        if(len(self.PrevTasksList)==0):
            return
        self.PrevTasksList[-1].UnExecuteTask()
        self.PrevTasksList.pop()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.OpenFile(
        r"C:\Users\FieryRMS\Downloads\289279279_1740174506323556_7478604231351854831_n.mp4")
    mainwindow.show()
    sys.exit(app.exec_())
