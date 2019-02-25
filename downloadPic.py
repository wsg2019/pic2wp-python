#coding=utf-8
'''
下载传入的图片链接，保存到目录tmp下，并按序号重命名
'''

import re
import os
import sys
import threading
from urllib import request

tmpDir="tmp\\"
fileList=[]
picLinkList=[]
index=0
threadLock = threading.Lock()

def downloadFile(url,fileName):
    '''
    下载图片，以指定名字命名
    '''
    request.urlretrieve(url, fileName)
    print('%s downloaded' %fileName)

def downloadJob(threadName):
    global picLinkList
    global index
    global fileList
    threadLock.acquire()
    while(len(picLinkList)>0):
        pic=picLinkList.pop()
        fileName=tmpDir+str(index)+'.jpg'
        index+=1
        fileList.append(fileName)
        threadLock.release()
        downloadFile(pic,fileName)
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

def downdloadPics(pLinkList):
    global picLinkList
    picLinkList=pLinkList
    downloadJobThread()
    return fileList
