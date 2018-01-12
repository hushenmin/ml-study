# -*- coding: utf-8 -*-
# Time    : 2018/1/12 10:21
# Author  : hushenmin
# Site    : 
# File    : trees.py
from math import log


class DevisionTree():
    print(__doc__)
    #创建数据集合，和对应的标签名称
    def create_dataset(self):
        #数据集合，1为真，0为假
        dataset = [
            [1, 1, 'yes'],
            [1, 1, 'yes'],
            [1, 0, 'no'],
            [0, 1, 'no'],
            [0, 1, 'no']
        ]
        #对应的标签名称
        labels = ['no surfacing', 'flippers']
        return dataset,labels

    #计算香农熵
    def calc_shannoent(self,dataset):
        #数据的条数，一条有三个维度，维度对应两个标签，一个分类结果。
        num_entries = len(dataset)
        #初始化一个字典，存放各个分类结果的数量。例如{yes:2,no:3},'yes'是鱼类出现2次，'no'不是鱼类出现3次
        labels_count = {}
        #遍历数据集合，每条数据的分类情况
        for feat_vec  in dataset:
            #因为分类结果在每条数据list的最后一个位置上，所以为-1
            current_label = feat_vec[-1]
            #统计一个条数,这里我是有疑问的？？？？？？
            if current_label not  in  labels_count.keys():
                labels_count[current_label] = 0
            labels_count[current_label] +=1
        #信息熵初始值0.0
        shannon_ent = 0.0
        #求信息熵，公式：H(x)=E[I(xi)]=E[log2 1/p(xi)]=-ξp(xi)log2 p(xi)(i=1,2,..n)
        for key in labels_count:
            prob = float(labels_count[key])/num_entries
            shannon_ent -= prob * log(prob,2)
        return shannon_ent

    #根据数据集中所有行的某一列为axis中查找所有包含值为value的行，并且过滤掉这个列的值
    def split_dataset(self,dataset,axis,value):
        #定义一个最后返回的列表
        res_dataset = []
        #遍历dataset的所有数据，找到特定列为axis，值为value的行
        for feat_vec in dataset:
            #判断值列axis的值是不是等于value
            if(value == feat_vec[axis]):
                #list拼接extend，append方法，将所有等于value的行选中，并且过滤这个列
                reduce_feat_vec = feat_vec[:axis]
                reduce_feat_vec.extend(feat_vec[axis+1:])
                res_dataset.append(reduce_feat_vec)
        return  res_dataset


    """
    根据最佳的特征标签进行分类。
    遍历所有的列，分别计算按照每个列进行分类的话的信息熵，因为每列中有不同的特征对象，
    因此需要对每个特征对象进行求信息熵，然后通过求该列所有特征对象的信息熵之和。
    比较每列求出的信息熵的和的大小，值越大，混乱的越大，值越小，混乱度越小。
    """
    def choose_bestfeature_tosplit(self,dataset):
        devision =  DevisionTree()
        feature_nums = len(dataset[0]) -1
        base_entropy = devision.calc_shannoent(dataset)
        best_infograin ,best_feature = 0.0,-1
        for feat_num in range(feature_nums):
            feature_list = [example[feat_num] for example in dataset]
            unique_feature = set(feature_list)
            new_entropy = 0.0
            for feature in unique_feature:
                sub_dataset = devision.split_dataset(dataset,feat_num,feature)
                prop = len(sub_dataset)/float(len(dataset))
                new_entropy += prop * devision.calc_shannoent(sub_dataset)
            infograin = base_entropy - new_entropy
            if(infograin > best_infograin):
                best_infograin = infograin
                best_feature = feat_num
        return best_feature
    """
    查找一个列表中，选择列表中出现次数最多的值返回。
    注意：主要用在当个维度为1的分类方法中。
    """
    def mojority_count(self,class_list):
        class_count = {}
        for  vote in class_list:
            if vote not in class_count.keys():
                class_count[vote] = 0
            class_count[vote] += 1
            import operator
        sort_labels_count = sorted(class_count.iteritems(),key=operator.itemgetter(1),reverse=True)
        return  sort_labels_count[0][0]
    """
    在使用决策树做分类的时候，往往有多个特征值，这就需要在父特征的分类条件下，依据子特征据需分类。
    因此就形成的决策树，{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}
    
    """

    def create_tree(self,dataset,labels):
        devision =  DevisionTree()
        feature_list  = [example[-1] for example in dataset]
        if feature_list.count(feature_list[0]) == len(feature_list):
            return feature_list[0]
        if len(dataset[0]) ==1:
            return  devision.mojority_count(feature_list)
        best_feature = devision.choose_bestfeature_tosplit(dataset)
        best_feature_lables = labels[best_feature]
        tree = {best_feature_lables:{}}
        #全局的，全局的，全局的，重要是事情说三遍！！！！
        del(labels[best_feature])
        feat_values = [example[best_feature] for example in dataset]
        unique_values = set(feat_values)
        for value in unique_values:
            sub_labels= labels[:]
            #巧妙的运用的split_dataset的方法，在父特征值的那个条件下，根据子特征值分类。
            tree[best_feature_lables][value]  = devision.\
                create_tree(devision.split_dataset(dataset,best_feature,value),sub_labels)
        ##print tree
        return tree
    #分类，根据决策树分类。例子：{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}
    #labels = ['no surfacing', 'flippers']
    def classify(self,input_tree,feature_lables,test_vec):
        devision = DevisionTree()
        #找到根的key.(no surfacing)
        first_key = input_tree.keys()[0]
        #找到根下面第二级字典( { 0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}} )
        second_dic = input_tree[first_key]
        #找到根的key在labels对应的索引位置(0)
        feature_index = feature_lables.index(first_key)
        #测试数据的该标签对应的数据
        key =test_vec[feature_index]
        #该数据作为下一个字典的key,找到该key对应的值
        feature_value = second_dic[key]
        print '+++', first_key, 'xxx', second_dic, '---', key, '>>>', feature_value
        #判断是不是还有dic类型的，如果有说明需要继续递归直到没有dic类型。如果没有dic类型，直接取字典的值即可。
        if isinstance(feature_value,dict):
            class_label = devision.classify(feature_value,feature_lables,test_vec)
        else:
            class_label = feature_value
        return class_label

    #序列化保存模型，方便以后使用。
    def store_tree(self,input_tree,file_name):
        import pickle
        with open(file_name,'w+') as fw:
            pickle.dump(input_tree,fw)
    #反序列话模型，调用决策树
    def grab_tree(self,file_name):
        import pickle
        with open(file_name,'w+') as fw:
            pickle.load(file_name)
    #测试
    def fish_test(self):
        devision = DevisionTree()
        my_dat,labels = devision.create_dataset()
        my_tree =  devision.create_tree(my_dat,labels)
        my_dat, labels = devision.create_dataset()
        print devision.classify(my_tree,labels,[0,0])
        #import decisionTreePlot as dtPlot

if __name__ == '__main__':
    devision = DevisionTree()
    devision.fish_test()
    #dataset,labels = devision.create_dataset()
    #print devision.calc_shannoent(dataset)
   # print devision.choose_bestfeature_tosplit(dataset)
    #print  devision.create_tree(dataset,labels)


















