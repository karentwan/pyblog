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

def findByCondition(sql, *args, conn = None):
    if not conn:
        conn = getConnector()
    cursor = getCursor(conn)
    cursor.execute(sql, args)
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values

def findOneByCondition(sql, *args, conn = None):
    if not conn:
        conn = getConnector()
    cursor = getCursor(conn)
    cursor.execute(sql, args)
    values = cursor.fetchone()
    cursor.close()
    conn.close()
    return values

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

