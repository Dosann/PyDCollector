# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 15:35:20 2017

@author: duxin
"""

import json

def path_combination(paths):
    pass
        

path=[]
path.append([['url','http://www.patentstar.cn/frmLogin.aspx'],
          ['input','//*[@id="TextBoxAccount"]@@{username}'],
          ['input','//*[@id="Password"]@@{passwd}'],
          ['click','//*[@id="ImageButtonLogin"]'],
          ['sleep',3],
          ['click','//*[@id="Smartnavbom"]/ul/li[1]/a'],
          ['click','//*[@id="listIPC"]/li[1]/a'],
          ['click','//*[@id="ipc_result"]/li[2]/div[3]/span[1]'],
          ['collect','//*[@id="divlist"]/ul/li[*]/div[1]/a@@href']])
path.append([['url','http://www.patentstar.cn/frmLogin.aspx'],
          ['input','//*[@id="TextBoxAccount"]@@{username}'],
          ['input','//*[@id="Password"]@@{passwd}'],
          ['sleep',2],
          ['click','//*[@id="ImageButtonLogin"]'],
          ['sleep',2],
          ['click','//*[@id="Smartnavbom"]/ul/li[1]/a'],
          ['click','//*[@id="listIPC"]/li[1]/a'],
          ['click','//*[@id="ipc_result"]/li[2]/div[3]/span[1]'],
          ['loopstart','],
          ])
      
path_json=json.dumps(path)
print path_json