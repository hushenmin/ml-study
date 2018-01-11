# -*- coding: utf-8 -*-
# Time    : 2018/1/10 21:00
# Author  : hushenmin
# Site    : 
# File    : dating_clazz.py
import numpy as np
from  numpy import  * 
import operator
from os import listdir
import os
import sys




class Dating_Clazz(object):

    def create_dataset(self):
        group = np.array([[1.0,1.1],[1.0,1.0],[0.,0.],[0.,0.1]])
        labels = ['A','A','B',"B"]
        return group,labels


    def classfy(self,inX,group,lables,k=1):
        #已知矩阵的行数
        group_size = group.shape[0]
        #矩阵各个元素之差
        diff_mat =  np.tile(inX,(group_size,1)) - group
        #取平方
        diff_sqr_mat= diff_mat ** 2
        #每一行各个元素求和
        diff_sqr_sum_mat= diff_sqr_mat.sum(axis=1)
        #开方
        distance_mat = diff_sqr_sum_mat ** 5
        #排序，将排序后的索引值取出赋值给列表
        distance_sort_list = distance_mat.argsort()
        #选择距离最小的K个点
        class_count_dic = {}
        for i in  range(k):
            #属于哪一个分类标签
            class_labels = lables[distance_sort_list[i]]
            #计算每个分类标签个数
            class_count_dic[class_labels] =  class_count_dic.get(class_labels,0) + 1
        #排序按域排序
        class_count_sort_dic = sorted(class_count_dic.items(), key=operator.itemgetter(1), reverse=True)
        return class_count_sort_dic[0][0]

    def file_tomat(self,file_name):
        #读文件
        with open(file_name,'r') as file:
            #文件的行数
            file_lines = len(file.readlines())
            #初始化一个零矩阵
            return_mat= zeros((file_lines,3))
            index = 0
            clazz_labels = []
            with open(file_name, 'r') as file:
                for line  in file.readlines():
                    line_list  = line.strip().split('\t')
                    return_mat[index,:] = line_list[:3]
                    clazz_labels.append(line_list[-1])
                    index += 1
        return return_mat,clazz_labels
    def auto_norm(self,dataset):
        #每列的最大值，最小值，以及极差
        value_min = dataset.min(0)
        value_max = dataset.max(0)
        ranges = value_max - value_min
        #初始化归一化矩阵
        dataset_norm = zeros(shape(dataset))
        #矩阵的行数
        col_num = dataset.shape[0]
        #归一化表达式
        dataset_norm = (dataset - tile(value_min,(col_num,1)))/tile(ranges,(col_num,1))
        return dataset_norm,ranges,value_min

    def dating_clazzfy_test(self,file_name_path):
        dating_clazz = Dating_Clazz()
        ho_ratio =  0.2
        #从文件中加载数据
        dating_clazz = Dating_Clazz()
        dataset_mat,labels  = dating_clazz.file_tomat(file_name_path)
        dataset_norm_mat,ranges,value_min = dating_clazz.auto_norm(dataset_mat)
        col_num = dataset_norm_mat.shape[0]
        dataset_train_num = int(col_num * ho_ratio)
        print 'dataset_mat',dataset_train_num
        erro_count = 0;
        for i in range(dataset_train_num):
            classfy_results = dating_clazz.classfy(dataset_norm_mat[i,:],dataset_norm_mat[dataset_train_num:col_num,:],labels[dataset_train_num:col_num],3)
            print "分类结果: %s, 真正的类别: %s" % (classfy_results, labels[i])
            if(classfy_results != labels[i]):
                erro_count +=1
        print "错误率: %d " %(erro_count/float(dataset_train_num))
        print erro_count

    def image_tomat(self,file_name):
        image_mat = zeros((1,1024))
        with open(file_name,'r') as fr:
            for i  in range(32):
                image_line = fr.readline()
                #print image_line
                for j in range(32):
                    image_mat[0,32*i + j] = int(image_line[j])
        return image_mat


    def classfy_handwriting_test(self,file_training_path,file_test_path):
        dating_clazz = Dating_Clazz()
        hwlabels = []
        hw_training_dataset_list = listdir(file_training_path)
        hw_image_number  =  len(hw_training_dataset_list)
        hw_training_mat = zeros((hw_image_number,1024))
        for  i in range(hw_image_number):
            file_name_str = hw_training_dataset_list[i]
            file_name_pre_str = file_name_str.split('.')[0]
            class_labels = int(file_name_pre_str.split('_')[0])
            hwlabels.append(class_labels)
            hw_training_mat[i,: ] = dating_clazz.image_tomat(file_training_path+"\\%s" % file_name_str)
            #print hw_training_mat,"==========",class_labels
        #测试数据
        hw_test_dataset_list = listdir(file_test_path)
        erro_count = 0.0
        hw_test_image_number = len(hw_test_dataset_list)
        for i in range(hw_test_image_number):
            hw_test_file_name_str = hw_test_dataset_list[i]
            hw_test_file_pre_str = hw_test_file_name_str.split('.')[0]
            hw_test_label = int(hw_test_file_pre_str.split('_')[0])
            hw_test_mat = dating_clazz.image_tomat(file_test_path  + "\\%s"% hw_test_file_name_str)
            hw_test_classfy_result = dating_clazz.classfy(hw_test_mat,hw_training_mat,hwlabels,3)
            print "分类结果: %s, 真正的类别: %s" % (hw_test_classfy_result, hw_test_label)
            if (hw_test_label != hw_test_classfy_result):
                erro_count += 1
        print "错误率: %d " % (erro_count / float(hw_test_image_number))
        print erro_count






if __name__ == '__main__':
    dating_clazz = Dating_Clazz()
    # group,labels = dating_clazz.create_dataset()
    # class_labels = dating_clazz.classfy([0,0],group,labels,2)
    # print class_labels
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    # path =  path+ "\\input\\2.KNN\\datingTestSet2.txt"
    # print path
    # dating_clazz.dating_clazzfy_test(path)
    # C:\Users\Administrator\PycharmProjects\ml-study\input\2.KNN\testDigits\0_0.txt
    #path = path + "\\input\\2.KNN\\testDigits\\0_0.txt"
    #print  dating_clazz.image_tomat(path)
    file_training_path = path + "\\input\\2.KNN\\trainingDigits"
    file_test_path = path + "\\input\\2.KNN\\testDigits"
    dating_clazz.classfy_handwriting_test(file_training_path,file_test_path)






