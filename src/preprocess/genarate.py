# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random

trainval_percent = 0.8   #trainval占整个数据集的百分比，剩下部分就是test所占百分比
train_percent = 0.7  # train占trainval的百分比，剩下部分就是val所占百分比
xmlfilepath = 'F:\SJJ/CA/data/VOCdevkit2007/VOC2007/Annotations'
txtsavepath = 'F:\SJJ/CA/data/VOCdevkit2007/VOC2007/ImageSets/Main'
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

ftrainval = open(txtsavepath+'/trainval.txt', 'w')
ftest = open(txtsavepath+'/test.txt', 'w')
ftrain = open(txtsavepath+'/train.txt', 'w')
fval = open(txtsavepath+'/val.txt', 'w')

for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()
