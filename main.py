from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import path
from sys import argv

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"/media/ziad/42107CB9107CB60F/zizo/projects/PYTHON/My_Downloader/main.ui"))


class mainapp(QMainWindow,FORM_CLASS):
    def __init__(self, parent=None):
        super(mainapp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(argv)
    MainWindow = QMainWindow()
    window = mainapp()
    window.show()
    app.exec()