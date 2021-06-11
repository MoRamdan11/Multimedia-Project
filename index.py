from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import cv2 as cv
import numpy as np
from DB import Database
import os
from featureExtraction import FeatureExtraction

MainUI, _ = loadUiType('design.ui')

DB = Database()
featureExtraction = FeatureExtraction()

class Main(QMainWindow, MainUI):
    def __init__(self, parent=None):
        self.image = []
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.load_query_image)
        self.comboBox.addItem('Mean Color Algorithm')
        self.comboBox.addItem('Histogram Algorithm')
        self.comboBox.addItem('Color Layout Algorithm')
        self.pushButton_2.clicked.connect(self.initDB)
        self.pushButton_3.clicked.connect(self.showResults)

    def compareHist(self, HQ, HM):  # HM is histogram of the Model Image
        diff = cv.compareHist(HQ, HM, cv.HISTCMP_INTERSECT)
        sum = 0
        for i in HM:
            sum = sum + i
        return diff / sum

    def showResults(self):
        selector = self.comboBox.currentText()
        if(selector == 'Mean Color Algorithm'):
            print(selector)
        elif(selector == 'Histogram Algorithm'):
            queryHist = featureExtraction.get_histogram(self.image)
            results = DB.histogram_find()
            matchedPaths = []
            for result in results:
                modelHist = np.float32(result['hist'])
                compare = self.compareHist(queryHist, modelHist)
                if compare > 0.5:
                    matchedPaths.append(result['path'])
                    print(result['path'])
            print('matched')
            print(matchedPaths)
            for path in matchedPaths:
                match = cv.imread('img/' + path)
                cv.imshow('res', match)
                cv.waitKey(0)
            cv.waitKey(0)
        elif(selector == 'Color Layout Algorithm'):
            matchedPaths = []
            queryHist = featureExtraction.get_color_layout(self.image) #List of 4 Lists
            results = DB.colorLayout_find()
            sum = 0
            for result in results:
                for i in range(len(queryHist)):
                    modelHist = np.float32(result['colorLayout'][i])
                    sum = sum + self.compareHist(queryHist[i], modelHist)
                avg = sum / 4
                if avg > 0.5:
                    matchedPaths.append(avg)
            for path in matchedPaths:
                match = cv.imread('img/' + path)
                cv.imshow('res', match)
                cv.waitKey(0)
            cv.waitKey(0)

    def load_query_image(self):
        img = QFileDialog.getOpenFileName(self, 'Open File')
        self.label.setPixmap(QtGui.QPixmap(img[0]))
        self.image = cv.imread(img[0])

    def initDB(self):
        path = "C:/Users/Mohamed Ramadan/PycharmProjects/multimedia/Github/img"  # Add images dataset full path
        DB.delete_all()
        path, dirs, images = next(os.walk(path))
        for imgPath in images:
            record = {
                "path": imgPath,
                "features": [],
            }
            img = cv.imread('img/' + imgPath)  # Read the image
            # 1- Mean Color Algorithm
            meanColor = featureExtraction.get_mean(img)
            record["features"].extend(meanColor)
            # 2- calculate the histogram
            histogram = featureExtraction.get_histogram(img)
            record["hist"] = histogram.tolist()
            # 3- Color layout Algorithm using histogram similarity
            colorLayout = featureExtraction.get_color_layout(img)
            colorLayoutList = []
            for quarter in colorLayout:
                colorLayoutList.append(quarter.tolist())
            record["colorLayout"] = colorLayoutList
            DB.insert(record)

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.setWindowTitle('CBRS')
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()