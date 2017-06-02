# -*- coding: utf-8 -*-
"""
Created on Thu Jun 08 10:07:11 2017

@author: duxin
"""

from sys import path
path.append('../../SpiderEngine')
path.append('../../SpiderEngine/core')
import GLOBAL
from Tools import GithubAccountManagement
import github

def createG(login=None,passwd=None,autofetch=None,conn=None):
    if login!=None and passwd!=None:
        g=github.Github(login,passwd,per_page=100)
        account=None
    elif autofetch!=None and conn!=None:
        account=GithubAccountManagement.OccupyAnAccount(conn)
        g=github.Github(account[1],account[2],per_page=100)
    return g,account

def getRepos(target,since=0):
    getrepos=target.get_repos(since=since)
    return getrepos

def releaseAccount(conn,account):
    if account==None:
        print('empty accout')
        return
    GithubAccountManagement.ReleaseAnAccount(conn,account)