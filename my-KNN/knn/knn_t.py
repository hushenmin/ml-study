# -*- coding: utf-8 -*-
import file2matrix
import os
import sys
import show_plt
path  = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
sys.path.append(path)

print str(path)
#path = os.path.dirname(os.path.abspath("."))
os.listdir(path)

show_plt(file2matrix.file2matrix("datingTestSet2.txt"))
