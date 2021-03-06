#! /usr/bin/env python
#-*- coding:utf-8 -*-

'''
数据库操作的类
'''

import mysql.connector as connector

def getConnector():
    conn = connector.connect(user='root', password='root', database='pyblog', use_unicode=True)
    return conn

def getCursor(con):
    return con.cursor()

def selectAll(cursor, table):
    cursor.execute('select * from %s',(table))
    values = cursor.fetchall()
    cursor.close()
    return values


def select( sql, conn = None):
    if not conn:
        conn = getConnector()
    cursor = getCursor(conn)
    cursor.execute(sql)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values

'''
返回带列名的数据集
'''
def findByCondition(sql, *args, conn = None):
    if not conn:
        conn = getConnector()
    print("sql:%s"%(sql))
    cursor = getCursor(conn)
    cursor.execute(sql, args)
    values = cursor.fetchall()
    result = []
    # 获取列的描述
    index = cursor.description
    # print("index:%s" % (index))
    for value in values:
        row = {}
        for i in range(len(index)):
            row[index[i][0]] = value[i]
        result.append(row)
    cursor.close()
    conn.close()
    return result

def findOneByCondition(sql, *args, conn = None):
    if not conn:
        conn = getConnector()
    cursor = getCursor(conn)
    cursor.execute(sql, args)
    index = cursor.description
    value = cursor.fetchone()
    result = {}
    for i in range(len(index)):
        result[index[i][0]] = value[i]
    cursor.close()
    conn.close()
    return result

def findone(sql, conn = None):
    if not conn:
        conn = getConnector()
    cursor = getCursor(conn)
    cursor.execute(sql)
    value = cursor.fetchone()
    cursor.close()
    conn.close()
    return value

'''
    @:param conn 数据库连接
    @:param sql 要执行的语句
    @:return count 返回受影响的行数
'''
def insert(sql, *args, conn = None):
    if not conn:
        conn = getConnector()
    cursor = getCursor(conn)
    cursor.execute(sql, args)
    count = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return count

