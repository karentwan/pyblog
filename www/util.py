#! /usr/bin/python env
#-*- coding:utf-8 -*-

import hashlib
import time

SUBCATEGORY = ['原', '转']



'''
数字转成子标签
'''
def number2Subcate(n):
    if n > len(SUBCATEGORY):
        n = 0
    return SUBCATEGORY[n]

def MD5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()

'''
时间戳转时间
'''
def timestamp2time(timestamp):
    # 打印时间戳
    print(timestamp)
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d", time_local)
    # dt = '2018-04-30'
    return dt

'''
将所有的列表里面的时间戳都转换为时间
@:param list 一个列表，每一个元素都是一个dict
'''
def timestamp2DateForAll(list):
    result = []
    # 将时间戳转换为时间
    for value in list:
        temp = dict()
        for k, v in value.items():
            if k == 'time':
                temp[k] = timestamp2time(v)
            else:
                temp[k] = v
        result.append(temp)
    return result

'''
第一个参数是没加密的
'''
def cmp_password(str1, str2):
    encode = MD5(str1)
    # print('encode:%s'%(encode))
    return encode == str2