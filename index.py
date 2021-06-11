from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

MainUI, _ = loadUiType('design.ui')


class Main(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.load_query_image)
        self.comboBox.addItem('Mean Color Algorithm')
        self.comboBox.addItem('Histogram Algorithm')
        self.comboBox.addItem('Color Layout Algorithm')

    def load_query_image(self):
        img = QFileDialog.getOpenFileName(self, 'Open File')
        self.label.setPixmap(QtGui.QPixmap(img[0]))




def main():
    app = QApplication(sys.argv)
    window = Main()
    window.setWindowTitle('CBRS')
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
