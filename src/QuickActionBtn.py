from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from pathlib import Path
import shutil
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
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
        print(f"could not copy {FilePath} to {self.DestDir}")
        return False

    def Move(self, FilePath):
        try:
            shutil.move(FilePath, self.DestDir)
            return True
        except FileNotFoundError:
            print("Error: No such file")
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
        print(f"could not move {FilePath} to {self.DestDir}")
        return False

    def Delete(self, FilePath):
        try:
            send2trash.send2trash(FilePath)
            return True
        except FileNotFoundError:
            print("Error: File not found")
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
        print(f"could not delete {FilePath}")
        return False

    # returns true if file is still present in original dir
    def ExecuteTask(self, FilePath):
        FilePath = str(Path(FilePath).resolve())
        if(self.Task(FilePath)):
            self.prevTasksList.append(FilePath)
            if(self.Task == self.Copy):
                return True
            return False
        else:  # handle errors
            pass
        return True

    def UnCopy(self, FilePath):
        DestFile = Path(self.DestDir).joinpath(Path(FilePath).name)
        return self.Delete(str(DestFile))

    def UnMove(self, FilePath):
        DestFile = Path(self.DestDir).joinpath(Path(FilePath).name)
        try:
            shutil.move(DestFile, FilePath)
            return True
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
        print(f"could not move {DestFile} to {FilePath}")
        return False

    def UnDelete(self, FilePath):
        try:
            winshell.undelete(FilePath)
            return True
        except ValueError:
            print("Error: File not found")
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
        print(f"Could not restore {FilePath} from trash")
        return False

    def UnExecuteTask(self):
        if(len(self.prevTasksList) == 0):
            return

        if(self.UnTask(self.prevTasksList[-1])):
            self.prevTasksList.pop()
        else:  # handle errors
            pass
