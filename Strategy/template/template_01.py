# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:24:55 2017
@author: duxin
Email: duxin_be@outlook.com

"""

from sys import path
path.append("../")
from core import Tools
from core import Spider
import Queue
import traceback
import re
import time
import json
from sys import exit as sexit

#@@import@@



def run(taskque,crawlerbody,errortasks):
    #从队列中获取任务，编写与该任务相关的信息提取代码
    #@@globalVariables@@
    
    conn=crawlerbody.conn
    driver=crawlerbody.driver
    
    #从队列中读取1个任务
    task=taskque.get()
    print task
    
    try:
        #print "url:%s"%(task[2]),len(task[2]),type(task[2])
        new_urls=turnToElement(driver,json.loads(task[2]))
        if task[1]<=1000000:
            
            data=[]
            for new_url in new_urls:
                if filterByDomain(new_url[0][1],domain_name,url_match_mode)!='pass':
                    continue
                current_id+=1
                new_url_json=json.dumps(new_url)
                taskque.put([current_id,task[1]+1,new_url_json])
                data.append([current_id,new_url_json,'unvisited'])
                
            Tools.SaveData.SaveData(conn,data,"%s"%(tname_urls),['id','url','status'])
            Tools.SaveData.UpdateData(conn,['visited'],"%s"%(tname_urls),['status'],'id=%s'%(task[0]))
    except Exception,e:
        #driver.get_screenshot_as_file('../files/screenshots/%s.jpg'%task[0])
        traceback.print_exc()
        print e
        print "error task %s has been put back to taskque"%(task[0])
        if hasattr(e,'reason') and hasattr(e.reason,'errno') and e.reason.errno==10061:
            sexit('errno:10061')
        return
        
        
        
def get_paras():
    #设置参数
    paras={}
    #数据库访问设置
    paras["conn_settings"]={"dbname":"sentiment",
                             'host':"rm-bp10rf4zreaw5he66o.mysql.rds.aliyuncs.com",
                             'user':'root',
                             'port':3306,
                             'passwd':'Csstsari107'}
    #线程数
    paras["threadnumber"]=5
    
    #不开启webdriver
    paras["webdriver"]="PhantomJS"
    paras["loadimage"]=False
    
    #使用github账号
    paras["github_account"]=None
    
    #是否自动创建表单
    paras["db_construction"]=True
         
    #Crawler对象的其他初始化操作(登陆之类的)
    paras["crawler_initialize"]=CrawlerInitialize
    
    #是否在redis中读写队列
    paras["taskque_format"]=None
    #paras["taskque_format"]="redis"
    #paras["redis_settings"]={"dbname":0,
    #                         "host":'120.25.107.34',
    #                         "port":6379}
    
    
    return paras


def create_queue():
    global initial_url,domain_name,urlset,current_id,ifrset,tname_urls
    
    initial_url=json.dumps([['url',initial_url]])
    conn=Tools.DatabaseSupport.GenerateConn(dbname='sentiment',host='rm-bp10rf4zreaw5he66o.mysql.rds.aliyuncs.com',user='root',port=3306,passwd='Csstsari107')
    temp=Tools.LoadData.LoadDataByCmd(conn,"select id,url from %s limit 1"%(tname_urls))
    if len(temp)==0:
        Tools.SaveData.SaveData(conn,[['%s'%(initial_url),'unvisited']],'%s'%(tname_urls),['url','status'])
    urls=Tools.LoadData.LoadDataByCmd(conn,"select id,url from %s where status='unvisited'"%(tname_urls))
    current_id=int(Tools.LoadData.LoadDataByCmd(conn,"select max(id) from %s"%(tname_urls))[0][0])
    
    
    conn.close()
    
    #创建队列
    que=Queue.Queue()
    print len(urls)
    if len(urls)==0:
        urlset=set(initial_url)
        task=(0,0,initial_url)
        que.put(task)
    else:
        urlset=set(map(lambda x:x[1],urls))
        for urlid,url in urls:
            que.put((urlid,0,url))
    
    return que

def CrawlerInitialize(crawlerbody):


def main(initial_url1,domain_name1,url_match_mode1,tname_urls1):
    global initial_url,domain_name,url_match_mode,tname_urls
    initial_url=initial_url1
    domain_name=domain_name1
    url_match_mode=url_match_mode1
    tname_urls=tname_urls1
    Spider.main(get_paras(),create_queue,run,mode=1)


main("""https://www.dianping.com/shanghai/food""",'dianping.com',url_match_mode1=2,tname_urls1='t_dianping')
# url_match_mode 1:全域名匹配(course.shlll.net) 2:匹配从第二格开始的部分(shlll.net) 3:匹配域名的全部部分(course.shlll.net/course)





