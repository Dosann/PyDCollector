# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 16:02:43 2017

@author: duxin
"""

import time
from string import strip

optionalMode=['githubapi','mysqlconn','pd_function']



def submodConstruction(path):
    
    pathLength=len(path)
    #确认mod运行时的手段：PhantomJS/staticweb/(optionalMode)/unknown
    crawlerMode=_crawlerMode(path,optionalMode)
    if crawlerMode=='unknown':
        return False
    
    #初始化代码段
    submod=_submodInitialize()
    #path所有相关的解析class
    relaPackages=set(map(lambda x:x.split('||')[0],path))
    submod+='from sys import path\n'
    submod+='path.append("../parse")\n'
    for relaPackage in relaPackages:
        submod+="import %s\n"%(relaPackage)
    submod+="\n"
    #解析path生成代码
    for i in range(pathLength):
        pace=path[i]
        funClass,function,obj,paras=_parsePace(pace)
        if obj=='':
            submod+="%s.%s(%s)\n"%(funClass,function,_parasTransform(paras))
        else:
            submod+="%s=%s.%s(%s)\n"%(obj,funClass,function,_parasTransform(paras))
    
    return submod

        
def _parsePace(pace):
    divide=pace.split('||')
    funClass,function,temp=divide
    divide_temp=temp.split('@@')
    obj=divide_temp[0]
    if len(divide_temp)==1 or strip(divide_temp[1])=='':
        paras=None
    else:
        mapping=map(lambda x:x.split('='),divide_temp[1].split('&'))
        paras=dict(mapping)
    return funClass,function,obj,paras

def _parasTransform(paras):
    if paras==None:
        return ''
    subs=[]
    for key,value in paras.items():
        value=value[0]=='$' and value[1:] or value
        subs.append('%s=%s'%(key,value))
        s=','.join(subs)
    return s

def _submodInitialize():
    submod='# -*- coding: utf-8 -*-\n\n'
    submod+='\"\"\"\n'
    submod+='Created: %s\n'%(time.ctime())
    submod+='@author: duxin\n'
    submod+='@email : duxin_be@outlook.com\n'
    submod+='Generated by PyDCollector\n\"\"\"\n\n'
    return submod



def _crawlerMode(path,optionalMode):
    tags=map(lambda x:x.split('||')[0],path)
    if 'click' in tags:
        return 'PhantomJS'
    elif 'url' in tags:
        return 'staticweb'
    else:
        tagheads=map(lambda x:x.split('@@')[0],tags)
        for mode in optionalMode:
            if mode in tagheads:
                return mode
        return 'unknown'

def _saveSubmod(submod,filename):
    with open(filename,'w') as f:
        f.write(submod)



path=['mysqlconn||mysqlOpen||conn@@host="rm-bp10rf4zreaw5he66o.mysql.rds.aliyuncs.com"&port=3306&dbname="testPyDCollector"&user="root"&passwd="Csstsari107"',
      'mysqlconn||mysqlOpen||connGA@@host="rm-bp10rf4zreaw5he66o.mysql.rds.aliyuncs.com"&port=3306&dbname="grabgithub"&user="root"&passwd="Csstsari107"',
      'mysqlconn||tryCreateTable||@@conn=$conn&tablename="repos"&columns="id int auto_increment primary key,reponame varchar(200)"',
      'githubapi||createG||g,account@@autofetch=True&conn=$connGA',
      'githubapi||getRepos||rps@@target=$g&since=0',
      'pd_function||pythonListTraverse||raw_data@@target=$rps&startid=0&endid=100',
      'pd_function||filterReponame||result@@target=$raw_data&startid=7&endid=22',
      'mysqlconn||mysqlSave||@@conn=$conn&data=$result&tablename="repos"&columns=["reponame"]',
      'githubapi||releaseAccount||@@conn=$connGA&account=$account',
      'mysqlconn||mysqlClose||@@conn=$conn',
      'mysqlconn||mysqlClose||@@conn=$connGA']
submod=submodConstruction(path)
print submod
_saveSubmod(submod,'submod/mod.py')