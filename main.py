
import gdal
import os
import sys
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from functools import reduce

from MoreOne import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QFileDialog,QApplication
from base_functions import drawMatchesKnn_cv2, save_matchedpoints_in_file

import sys

class myWindow(QDialog, Ui_Dialog):
    def __init__(self):
        super(myWindow,self).__init__()
        self.setupUi(self)

    def sopen1(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                    "选取文件",
                                    "/home/scrc/",
                                    "image Files (*.tif);;All Files (*)")
        self.lineEdit_one.setText(fileName)

    def sopen2(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         "选取文件",
                                                         "/home/scrc/",
                                                         "image Files (*.tif);;All Files (*)")
        self.lineEdit_two.setText(fileName)


    def sok(self):
        filename_first=self.lineEdit_one.text()
        filename_second = self.lineEdit_two.text()
        root = os.path.split(filename_first)[0]

        temp = list(filter(str.isdigit, os.path.split(filename_first)[1]))
        s_1 = reduce(lambda x, y:str(x)+str(y), temp)
        temp = list(filter(str.isdigit, os.path.split(filename_second)[1]))
        s_2 = reduce(lambda x, y: str(x)+str(y), temp)
        #    print ("{}_{}".format(s_1,s_2))
        # textfile = "{}_{}.txt".format(s_1, s_2)

        dataset = gdal.Open(filename_first)
        if dataset == None:
            print(filename_first + '文件无法打开')
            sys.exit(1)
        im_width = dataset.RasterXSize
        im_height = dataset.RasterYSize
        im_bands = dataset.RasterCount

        if not 1 == im_bands:
            print("image bands > 1")
            sys.exit(0)

        im_data = dataset.ReadAsArray(0, 0, im_width, im_height)
        del dataset

        img_1 = im_data.astype(np.uint8)
        img_ss = np.zeros((im_height, im_width, 3), dtype=np.uint8)
        for i in range(3):
            img_ss[:, :, i] = img_1

        dataset_2 = gdal.Open(filename_second)
        if dataset_2 == None:
            print(filename_second + '文件无法打开')
            sys.exit(1)
        im_width_2 = dataset_2.RasterXSize
        im_height_2 = dataset_2.RasterYSize
        im_data_2 = dataset_2.ReadAsArray(0, 0, im_width_2, im_height_2)
        del dataset_2

        img_2 = im_data_2.astype(np.uint8)
        img_sp = np.zeros((im_height_2, im_width_2, 3), dtype=np.uint8)
        for i in range(3):
            img_sp[:, :, i] = img_2

        """
        采用sift算子，提取匹配点，并存放到TXT文件中
        """
        # sift = cv2.xfeatures2d.SIFT_create()
        orb = cv2.ORB_create(5000)
        kp1, des1 = orb.detectAndCompute(img_ss, None)
        kp2, des2 = orb.detectAndCompute(img_sp, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        # bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)

        goodMatch = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                goodMatch.append(m)

        num_matched_point = len(goodMatch)
        print("匹配的点有{}个".format(num_matched_point))
        if num_matched_point < 2:
            print("match point less than 2")
            # continue

        imgfile = "{}_{}.png".format(s_1, s_2)
        out_img_file = os.path.join(root, imgfile)
        drawMatchesKnn_cv2(img_ss, kp1, img_sp, kp2, goodMatch, out_img_file)

        textfile = "{}_{}.txt".format(s_1, s_2)
        out_txt_file = os.path.join(root, textfile)
        save_matchedpoints_in_file(im_data, kp1, im_data_2, kp2, goodMatch, out_txt_file)


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = myWindow()
    window.show()
    sys.exit(app.exec_())
