# -*- coding: utf-8 -*-
# Time    : 2018/1/10 20:01
# Author  : hushenmin
# Site    : 
# File    : auto_norm.py
"""
    Desc:
        归一化特征值，消除特征之间量级不同导致的影响
    parameter:
        dataSet: 数据集
    return:
        归一化后的数据集 normDataSet. ranges和minVals即最小值与范围，并没有用到
    归一化公式：
        Y = (X-Xmin)/(Xmax-Xmin)
        其中的 min 和 max 分别是数据集中的最小特征值和最大特征值。该函数可以自动将数字特征值转化为0到1的区间。
    """
import numpy as np
import knn.file2matrix
import sys
import  os
def auto_norm(dataset):
    #计算矩阵每列的最大值，最小值，范围
    number_min =  dataset.min(0)
    number_max = dataset.max(0)
    #求极差
    ranges = number_max - number_min
    norm_dataset = np.zeros(np.shape(dataset))
    m = dataset.shape[0]
    #与最小值的差组成的矩阵
    norm_dataset = dataset - np.tile(number_min,(m,1))
    #最小值之差除以范围 归一化
    norm_dataset = norm_dataset/np.tile(ranges,(m,1))
    return norm_dataset,ranges,number_min
if __name__ == '__main__':
    pwd = os.getcwd()
    dataset_path = os.path.abspath(os.path.dirname(pwd)+'\knn\datingTestSet2.txt')
    return_mat,class_labels = knn.file2matrix.file2matrix(dataset_path)
    #print return_mat
    norm_dataset, range, number_min = auto_norm(return_mat)
    print norm_dataset


