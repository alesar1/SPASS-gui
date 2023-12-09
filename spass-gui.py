import subprocess
from PyQt6.QtWidgets import *
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)
        self.show()

        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_As.triggered.connect(self.saveFileAs)
        self.actionExit.triggered.connect(self.close)
        self.actionRun.triggered.connect(self.runCode)

    def openFile(self):
        global filename
        filename = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        if filename[0] == "":
            return
        f = open(filename[0], "r")
        with f:
            data = f.read()
            self.textSrcCode.setText(data)

    def saveFile(self):
        global filename
        try:
            f = open(filename[0], "w")
            with f:
                text = self.textSrcCode.toPlainText()
                f.write(text)
        except:
            print("No file opened")
            message = QMessageBox()
            message.setText("No File Opened")
            message.exec()

    def saveFileAs(self):
        global filename
        if self.textSrcCode.toPlainText() == "":
            print("No text to save")
            message = QMessageBox()
            message.setText("No Text to Save")
            message.exec()
            return
        filename = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*.*)")
        if filename[0] == "":
            return
        f = open(filename[0], "w")
        with f:
            text = self.textSrcCode.toPlainText()
            f.write(text)

    def runCode(self):
        code = self.textSrcCode.toPlainText()
        result = subprocess.run(
            ["SPASS", "-Stdin"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            input=code.encode("utf-8"),
        )
        if result.returncode == 0:
            self.textOutput.setText(result.stdout.decode("utf-8"))
        else:
            self.textOutput.setText("Error: " + result.stderr.decode("utf-8"))


def main():
    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle("SPASS")
    app.exec()


if __name__ == "__main__":
    main()