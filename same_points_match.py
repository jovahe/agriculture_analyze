#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 10:28:52 2018

@author: scrs
"""

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
from functools import reduce


# 读取文件夹下的所有图像
# debug in test2.py
def get_image_filenames(file_dir, file_type='.tif'):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == file_type:
                L.append(os.path.join(root, file))
    return L


def get_file_positon(imagenames):
    """
    根据图像名称中的数字，对imagenames的位置进行排序，返回imagenames的位置顺序
    """
    num_files = len(imagenames)
    if num_files < 2:
        print("file number is less than 2\n")
        sys.exit(0)

    tt = []
    for index, filename in enumerate(imagenames):
        #        print ("\n{}:{}".format(index, filename))
        tone = list(filter(str.isdigit, os.path.split(filename)[1]))
        xone = reduce(lambda x, y: str(x) + str(y), tone)
        temp = int(xone)
        #        print (temp)
        tt.append(temp)
    b = sorted(tt)
    inedxx = []
    for i in range(num_files):
        indtemp = tt.index(b[i])
        inedxx.append(indtemp)
    # print (inedxx)
    return inedxx


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


# 主函数 main

# base_root = "/home/scrs/PycharmProjects/agriculture_analyze/data/"
root = "/home/scrs/PycharmProjects/agriculture_analyze/data/"
# ss_list = os.listdir(base_root)
# ss_list, _, _ = os.walk(base_root)

# 检查ss_list是否全文件夹，把文件元素去掉
# dirlist = []
# for str_0 in ss_list:
#     str_0 = os.path.join(base_root, str_0)
#     if os.path.isdir(str_0):
#         dirlist.append(str_0)


# # 得到绝对路径list
# file_root = []
# for tp_list in dirlist:
#     temp_list = os.path.join(base_root, tp_list)
#     file_root.append(temp_list)
# # print (file_root)

print("root:{}".format(root))

originalImages = get_image_filenames(root)

ts = get_file_positon(originalImages)  # 对图像按照编号进行排序

print("order : {}".format(ts))

for index in range(len(originalImages) - 1):
    filename_first = originalImages[ts[index]]
    filename_second = originalImages[ts[index + 1]]
    print(filename_first, filename_second)
    temp = filter(str.isdigit, os.path.split(filename_first)[1])
    s_1 = reduce(lambda x, y: str(x) + str(y), temp)
    temp = filter(str.isdigit, os.path.split(filename_second)[1])
    s_2 = reduce(lambda x, y: str(x) + str(y), temp)
    #    print ("{}_{}".format(s_1,s_2))
    textfile = "{}_{}.txt".format(s_1, s_2)
    print(textfile)

    """
    打开两幅影像，转化成opencv可以处理的格式
    """
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
        continue

    imgfile = "{}_{}.png".format(s_1, s_2)
    out_img_file = os.path.join(root, imgfile)
    drawMatchesKnn_cv2(img_ss, kp1, img_sp, kp2, goodMatch, out_img_file)

    textfile = "{}_{}.txt".format(s_1, s_2)
    out_txt_file = os.path.join(root, textfile)
    save_matchedpoints_in_file(im_data, kp1, im_data_2, kp2, goodMatch, out_txt_file)
