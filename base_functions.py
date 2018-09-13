
"""
此程序为农科院刘轲博士编写，用于高光谱图像的同名点匹配与提取
采用opencv sift或surf算子进行特征点匹配
"""

# import re
import gdal
import os
import sys
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def drawMatchesKnn_cv2(img1_gray, kp1, img2_gray, kp2, goodMatch, outputfile):
    h1, w1 = img1_gray.shape[:2]
    h2, w2 = img2_gray.shape[:2]

    vis = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
    vis[:h1, :w1] = img1_gray
    vis[:h2, w1:w1 + w2] = img2_gray

    p1 = [kpp.queryIdx for kpp in goodMatch]
    p2 = [kpp.trainIdx for kpp in goodMatch]

    post1 = np.int32([kp1[pp].pt for pp in p1])
    post2 = np.int32([kp2[pp].pt for pp in p2]) + (w1, 0)

    for (x1, y1), (x2, y2) in zip(post1, post2):
        cv2.line(vis, (x1, y1), (x2, y2), (0, 0, 255))
        print(x1, y1, img1_gray[y1, x1, 1])
        print(x2 - w1, y2, img2_gray[y2, x2 - w1, 1])

    img_save = Image.fromarray(vis)
    img_save.save(outputfile)
    plt.imshow(vis)
    plt.show()


def save_matchedpoints_in_file(img1, kp1, img2, kp2, goodMatch, outputfile):
    p1 = [kpp.queryIdx for kpp in goodMatch]
    p2 = [kpp.trainIdx for kpp in goodMatch]

    post1 = np.int32([kp1[pp].pt for pp in p1])
    post2 = np.int32([kp2[pp].pt for pp in p2])

    with open(outputfile, 'w') as f:
        for (x1, y1), (x2, y2) in zip(post1, post2):
            f.write("{x1},{y1},{d1}, {x2},{y2},{d2}\t\n".format(x1=x1, y1=y1, d1=img1[y1, x1], x2=x2, y2=y2,
                                                                d2=img2[y2, x2]))