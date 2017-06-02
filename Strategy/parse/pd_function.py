# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 15:31:10 2017

@author: duxin
"""
from sys import path
path.append('../../SpiderEngine')
path.append('../../SpiderEngine/core')
import GLOBAL

def pythonListTraverse(target,startid=0,endid=None,unlimited=None):
    if unlimited==None or endid!=None:
        raw_data=[""]*(endid-startid)
        for i in range(startid,endid):
            raw_data[i-startid]=target[i]
    else:
        raw_data=[]
        for d in target[startid:]:
            raw_data.append(d)
    return raw_data

def filterReponame(target,startid=0,endid=None):
    result=map(lambda x:unicode(x),target)
    result=map(lambda x:[x[22:-2]],result)
    return result

#filterReponame(target=raw_data,startid=22,endid=-2)