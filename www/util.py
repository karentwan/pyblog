#! /usr/bin/python env
#-*- coding:utf-8 -*-

import hashlib

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
第一个参数是没加密的
'''
def cmp_password(str1, str2):
    encode = MD5(str1)
    return encode == str2