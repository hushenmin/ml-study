# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt
import file2matrix
import numpy  as np
def show_plt(path):
    return_max,class_labels = file2matrix.file2matrix(path)
    #构造一个figure对象，创建一副图
    plt_figure = plt.figure()
    #第一幅图的第一个字图
    ax = plt_figure.add_subplot(111)
    ax.scatter(return_max[:, 1], return_max[:, 2], 10.0*np.array(class_labels), 10.0* np.array(class_labels))
    plt.title('basic scatter plot ')
    plt.xlabel('variables x')
    plt.ylabel('variables y')

    plt.legend(loc='upper right')  # 这个必须有，没有你试试看

    plt.show()  # 这个可以没有



