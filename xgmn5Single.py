#coding=utf-8
'''
一、下载xgmn5.com中指定链接下的图片
使用如下
python xgmn5.py https://www.xgmn5.com/MiiTao/MiiTao10569.html

二、在项目pic2wp中使用获取图片链接以及标题
'''

import re
import os
import sys
import threading
from urllib import request
from bs4 import BeautifulSoup
import smms

site='https://www.xgmn5.com'
picLinkList = []
pageLink=[]
picLinkList=[]
index=1
threadLock = threading.Lock()
title=''

def getHtml(url):
    '''
    返回网页文本
    '''
    response=request.urlopen(url)
    page=response.read()
    return page

def getLink_title(html):
    '''
    获取其他页面的链接以及标题
    '''
    soup=BeautifulSoup(html,'html.parser',from_encoding='gb18030')
    title=soup.title.string
    x=soup.find_all(name='div',attrs={"class":"page"})
    reg=r'<a href="(.*?)"'
    linkre=re.compile(reg)
    linklist=linkre.findall(str(x))
    linklist1=[]
    for link in linklist:
        if link not in linklist1:
            linklist1.append(link)
    linklist1.append(title)
    return linklist1

def getPicLink(html):
    '''
    提取当前页面中的图片链接
    '''
    soup=BeautifulSoup(html,'html.parser',from_encoding='gb18030')
    x=soup.find_all(name='div',attrs={"class":"img"})
    reg=r'src="(.*?)"'
    picre=re.compile(reg)
    piclist=picre.findall(str(x))
    return piclist

def downloadPic(url,fileName):
    '''
    下载图片，以指定名字命名
    '''
    request.urlretrieve(url, fileName)
    print('%s downloaded' %fileName)

def downloadJob(threadName):
    global picLinkList
    global index
    threadLock.acquire()
    while(len(picLinkList)>0):
        pic=picLinkList.pop()
        fileName=str(index)+'.jpg'
        index+=1
        threadLock.release()
        downloadPic(site+pic,fileName)
        threadLock.acquire()
    threadLock.release()

class picThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("开启pic线程： " + self.name)
        downloadJob(self.name)
        print ("结束pic线程： " + self.name)

def downloadJobThread():
    th=[]
    for i in range(15):
        t = picThread(i, "Thread-%d" %i)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    print('图片下载结束')

def getPageLink(threadName):
    global picLinkList
    global pageLink
    threadLock.acquire()
    while(len(pageLink)>0):
        tmpPageLink=pageLink.pop()
        threadLock.release()
        page=getHtml(site+tmpPageLink)
        tmpPicLink=getPicLink(page)
        for a in tmpPicLink:
            picLinkList.append(a)
        threadLock.acquire()
    threadLock.release()

class pageThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("开启page线程： " + self.name)
        getPageLink(self.name)
        print ("结束page线程： " + self.name)

def getPageLinkThread():
    global title
    th=[]
    for i in range(5):
        t = pageThread(i, "Thread-%d" %i)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    print('%s页面下载结束' %title)

'''
下载对应链接下的所有图片
'''
def getAlbum(url):
    global picLinkList
    global index
    global pageLink
    global title
    page=getHtml(url)
    link_title=getLink_title(page)
    title=link_title.pop()
    if(os.path.exists(title)==False):
        os.makedirs(title)
    else:
        print('%s已经存在' %title)
        return
    os.chdir(title)
    pageLink=link_title
    picLinkList=getPicLink(page)
    getPageLinkThread()
    print(picLinkList)
    index=1
    downloadJobThread()

'''
获取图片链接以及标题，返回列表，最后一项是标题
'''
def getxgmn5AlbumPicLinkAndTitle(url):
    global picLinkList
    global index
    global pageLink
    global title
    page=getHtml(url)
    link_title=getLink_title(page)
    title=link_title.pop()
    pageLink=link_title
    picLinkList=getPicLink(page)
    getPageLinkThread()
    tmpPicLinkList=[]
    for x in picLinkList:
        tmpPicLinkList.append(site+x)
    tmpPicLinkList.append(title)
    return tmpPicLinkList

if __name__ == '__main__':
    getAlbum(sys.argv[1])
    #getAlbum('https://www.xgmn5.com/Xiuren/Xiuren10620.html')
    #print(getAlbumPicLinkAndTitle('https://www.xgmn5.com/Xiuren/Xiuren10620.html'))
