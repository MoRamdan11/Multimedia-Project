import cv2 as cv
import imutils
import numpy as np
class FeatureExtraction:
    def __init__(self):
        self.bins = (8, 12, 4)

    def get_mean(self, image):
        img2_av_R = np.mean(image[:, :, 2])
        img2_av_G = np.mean(image[:, :, 1])
        img2_av_B = np.mean(image[:, :, 0])
        return [img2_av_R, img2_av_G, img2_av_B]

    def crop_vertical(self, img):
        width = img.shape[1]
        widthCutOff = width // 2
        leftImg = img[:, 0: widthCutOff]
        rightImg = img[:, widthCutOff:]
        return (leftImg, rightImg)

    def crop_horrizonal(self, img):
        height = img.shape[0]
        heightCutOff = height // 2
        upperImg = img[0: heightCutOff, :]
        lowerImg = img[heightCutOff:, :]
        return (upperImg, lowerImg)

    def crop_img(self, img, numOfCuts):
        (leftImg, rightImg) = self.crop_vertical(img)
        (firstQuarter, thirdQuarter) = self.crop_horrizonal(leftImg)
        (secondQuarter, forthQuarter) = self.crop_horrizonal(rightImg)
        return [firstQuarter, secondQuarter, thirdQuarter, forthQuarter]

    def get_color_layout(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        features_vector = []
        layouts = self.crop_img(image, 0)
        for i in layouts:
            hist = self.histogram(i, None)
            features_vector.append(hist)
        return features_vector

    def get_histogram(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        return self.histogram(image, None)

    def histogram(self, image, mask=None):
        histogram = cv.calcHist([image], [0, 1, 2], mask, self.bins,
                                [0, 180, 0, 256, 0, 256])
        histogram = cv.normalize(histogram, histogram).flatten()
        # if imutils.is_cv2():
        #     histogram = cv.normalize(histogram).flatten()
        # else:
        #     histogram = cv.normalize(histogram, histogram).flatten()
        return histogram

# descriptor = FeatureExtraction()
# img = cv.imread('images/Salah2.jpg')
# #img = cv.resize(img, (600, 500), interpolation=cv.INTER_AREA)
# img2 = cv.imread('images/salah1.jpg')
# img2 = cv.resize(img2, (600, 500), interpolation=cv.INTER_AREA)
# v1 = descriptor.histogram(img, (8, 12, 4), None)
# v2 = descriptor.histogram(img2, (8, 12, 4), None)
# # print(v1)
# # print('-------------------------')
# # print(v2)
def compareHist(HQ, HM): #HM is histogram of the Model Image
    diff = cv.compareHist(HQ, HM, cv.HISTCMP_INTERSECT)
    sum = 0
    for i in HM:
        sum = sum + i
    return diff / sum

# diff = compareHist(v1, v2)
# print(diff)
# # sum = 0
# # for i in v2:
# #     sum = sum + i
# # print('sum', sum)
# # diff = cv.compareHist(v1, v2, cv.HISTCMP_INTERSECT)
# # print(diff / sum)