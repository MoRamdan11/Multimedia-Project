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
        meanColor = featureExtraction.get_mean(self.image)
        matchedPaths = []
        if selector == 'Mean Color Algorithm':
            results = DB.mean_color_find2()
            for result in results:
                if ((meanColor[0] >= 0.8 * result['features'][0]) and (meanColor[0] <= 1.2 * result['features'][0])) \
                        and (
                        (meanColor[1] >= 0.8 * result['features'][1]) and (meanColor[1] <= 1.2 * result['features'][1])) \
                        and ((meanColor[2] >= 0.8 * result['features'][2]) and (
                        meanColor[2] <= 1.2 * result['features'][2])):
                    print('query', meanColor)
                    print('model', result['features'])
                    matchedPaths.append(result['path'])
            for path in matchedPaths:
                match = cv.imread('img/' + path)
                cv.imshow('res', match)
                cv.waitKey(0)
            cv.waitKey(0)
        elif selector == 'Histogram Algorithm':
            queryHist = featureExtraction.get_histogram(self.image)
            results = DB.histogram_find()
            matchedPaths = []
            for result in results:
                modelHist = np.float32(result['hist'])
                compare = self.compareHist(queryHist, modelHist)
                if compare > 0.3:
                    matchedPaths.append(result['path'])
                    print(result['path'])
            print('matched')
            print(matchedPaths)
            for path in matchedPaths:
                match = cv.imread('img/' + path)
                cv.imshow('res', match)
                cv.waitKey(0)
            cv.waitKey(0)
        elif selector == 'Color Layout Algorithm':
            matchedPaths = []
            queryHist = featureExtraction.get_color_layout(self.image)  # List of 4 Lists
            results = DB.colorLayout_find()
            print(results[0]["colorLayout"][0])

            for result in results:
                sum = 0
                for i in range(len(queryHist)):
                    modelHist = np.float32(result['colorLayout'][i])
                    sum = sum + self.compareHist(queryHist[i], modelHist)

                avg = sum / 4
                print(avg)
                if avg > 0.3:
                    matchedPaths.append(result['path'])
                print(len(matchedPaths))
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
