# -*- coding: utf-8 -*-
"""
Created on Thu Jun 08 09:34:53 2017

@author: duxin
"""

from sys import path
path.append('../../SpiderEngine')
path.append('../../SpiderEngine/core')
import GLOBAL
from Tools import LoadData
from Tools import SaveData
from Tools import DatabaseSupport

def mysqlOpen(host=GLOBAL.mysqlHost,port=GLOBAL.mysqlPort,user=GLOBAL.mysqlUser,
              passwd=GLOBAL.mysqlPasswd,dbname=GLOBAL.mysqlDbname,charset=GLOBAL.mysqlCharset):
    conn=DatabaseSupport.GenerateConn(host=host,port=port,user=user,
                                      passwd=passwd,dbname=dbname,charset=charset)
    return conn

def mysqlClose(conn):
    conn.close()

def tryCreateTable(conn,tablename,columns):
    tables=LoadData.LoadDataByCmd(conn,'show tables')
    tables=map(lambda x:x[0],tables)
    if tablename not in tables:
        cmd='create table %s(%s)'%(tablename,columns)
        _executeCmd(conn,cmd)
        
def mysqlSave(conn,data,tablename,columns):
    SaveData.SaveData(conn,data,tablename,columns)

def _executeCmd(conn,cmd):
    cursor=conn.cursor()
    result=cursor.execute(cmd)
    cursor.close()
    return result