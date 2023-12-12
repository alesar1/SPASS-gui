#!/usr/bin/env python3

import subprocess
import sys

from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox

from ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_As.triggered.connect(self.saveFileAs)
        self.actionExit.triggered.connect(self.close)
        self.actionRun.triggered.connect(self.runCode)

    def openFile(self):
        global filename
        fn = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        if fn[0] == "":
            return
        filename = fn
        with open(filename[0], "r") as f:
            data = f.read()
            self.textSrcCode.setText(data)
        self.statusBar().showMessage("File Opened: " + filename[0])

    def saveFile(self):
        global filename
        if filename[0] == "":
            print("No file opened")
            message = QMessageBox()
            message.setText("No File Opened")
            message.exec()
            return
        if self.textSrcCode.toPlainText() == "":
            print("No text to save")
            message = QMessageBox()
            message.setText("No Text to Save")
            message.exec()
            return
        with open(filename[0], "w") as f:
            text = self.textSrcCode.toPlainText()
            f.write(text)
        self.statusBar().showMessage("File Saved: " + filename[0])

    def saveFileAs(self):
        global filename
        if self.textSrcCode.toPlainText() == "":
            print("No text to save")
            message = QMessageBox()
            message.setText("No Text to Save")
            message.exec()
            return
        fn = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*.*)")
        if filename[0] == "":
            return
        filename = fn
        with open(filename[0], "w") as f:
            text = self.textSrcCode.toPlainText()
            f.write(text)
        self.statusBar().showMessage("File Saved: " + filename[0])

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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("SPASS")
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
