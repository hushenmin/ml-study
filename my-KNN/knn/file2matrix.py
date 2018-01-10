# -*- coding: utf-8 -*-

import  numpy as np
import numpy
import os
import sys
path  = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
sys.path.append(path)
file_name = path+'\datingTestSet2.txt'
def file2matrix(file_name=file_name):
    """
    :param file_name: datingTestSet.txt文件路径
    :return: 数据矩阵(matrix)和矩阵对应的标签（labels）
    """
    with open(file_name,'r') as fr:
        # 获取文件行数
        lines_number = len(fr.readlines())
        #生成对应矩阵元素为0的矩阵 zeros(2，3)就是生成一个 2*3的矩阵，各个位置上全是 0
        return_mat = np.zeros((lines_number,3),dtype='float',)
        #定义标签列表
        class_labels = []
        #index 定义数据的循环行号
        index = 0
        with open(file_name, 'r') as fr:
            for line in fr.readlines():
                #移除字符串头尾指定的字符生成的新字符串  str.strip([chars])
                line = line.strip()
                # 以'\t'切割列
                line_list = line.split('\t')
                # 每列的属性数据
                #line_list =  [map(float, v) for v in line_list]
                return_mat[index,: ] = line_list[0:3]
                #print line_list[0:3]
                # 最后一列就是标签,标签int转型
                class_labels.append(int(line_list[-1]))
                # 行号+1递增
                index +=1
            return return_mat,class_labels
if __name__ == '__main__':
    return_mat,class_labels = file2matrix("datingTestSet2.txt")
    print return_mat



