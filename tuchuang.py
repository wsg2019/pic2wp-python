#coding=utf-8
'''
将相应的图片文件上传，返回图片链接
调用upload(inUploadFlag,inFileList)
第一个参数指定图床
    0：sm.ms
    1：siimg一类的
    2：chevereto一类的（pic303.com）
第二个参数指定图片文件列表
'''

import requests
from requests_toolbelt import MultipartEncoder
import json
from bs4 import BeautifulSoup
import time
import re
import threading

threadLock = threading.Lock()
fileList=[]
picLinkList=[]
uploadFlag=0
userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"


class chevereto: #pic303.com 一类的图床网站
    site=''
    header = {}
    s=requests.session()
    auth=[]
    loginTitle=''
    def __init__(self,site):
        self.header={"origin":site,"Referer": site,'User-Agent': userAgent}
        self.site=site

    def login(self,userName,pwd):
        x=self.s.get(self.site)
        reg=r'name="auth_token" value="(.*?)"'
        authre=re.compile(reg)
        self.auth=authre.findall(x.text)
        data={'auth_token':self.auth[0],'login-subject':userName,'password':pwd}
        response=self.s.post(self.site+'/login',data=data,headers=self.header)
        soup=BeautifulSoup(response.text,'html.parser')
        self.loginTitle=soup.title.string
        if self.loginTitle.find('登录')!=-1 or self.loginTitle.find('Sign in')!=-1:
            return False
        return True

    def upload(self,fileName):
        field={'source':('1.jpg',open(fileName,'rb'),'image/jpeg'),
                'type':'file',
                'action':'upload',
                'timestamp':str(int(time.time()))+"123",
                'auth_token':self.auth[0],
                'nsfw':'0'}
        m = MultipartEncoder(fields=field)
        self.header={"origin":self.site,"Referer": self.site,'User-Agent': userAgent,'Content-Type': m.content_type}
        response=self.s.post(self.site+'/json',data=m,headers=self.header)
        jsonData=json.loads(response.text)
        a=jsonData["image"]["url"]
        print(a)
        if(a==''):
            return ''
        return a

pic303=chevereto("http://pic303.com")


def smmsUpload(fileName):
    m = MultipartEncoder(fields={'smfile':('1.jpg',open(fileName,'rb'),'image/jpeg')})
    r=requests.post('https://sm.ms/api/upload',data=m,headers={'Content-Type': m.content_type})
    jsonData=json.loads(r.text)
    if(jsonData['code']=='error'):
        return ''
    return jsonData['data']['url']


def siimgUpload(fileName):
    m = MultipartEncoder(fields={'Filedata':('1.jpg',open(fileName,'rb'),'image/jpeg')})
    r=requests.post('https://www.skuimg.com/upload.php',data=m,headers={'Content-Type': m.content_type})
    print(r.text)
    picLink='https://www.skuimg.com/'
    reg=r':(.*?),'
    picre=re.compile(reg)
    a=picre.findall(str(r.text))
    if a[0]=='':
        return ''
    picLink=picLink+a[0]
    reg=r',(.*?),'
    picre=re.compile(reg)
    a=picre.findall(str(r.text))
    picLink=picLink+a[0]
    print(picLink)
    return picLink




def uploadSingle(fileName):
    global pic303
    if(uploadFlag==0):
        return smmsUpload(fileName)
    elif(uploadFlag==1):
        return siimgUpload(fileName)
    elif(uploadFlag==2):
        return pic303.upload(fileName)


def uploadJob(threadName):
    global fileList
    global picLinkList
    threadLock.acquire()
    while(len(fileList)>0):
        fileName=fileList.pop()
        threadLock.release()
        pLink=uploadSingle(fileName)
        if pLink=="":
            print(fileName+"上传失败")
        else:
            print(fileName+"已经上传")
        threadLock.acquire()
        picLinkList.append(pLink)
    threadLock.release()

class uploadThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("开启upload线程： " + self.name)
        uploadJob(self.name)
        print ("结束upload线程： " + self.name)

def upload(inUploadFlag,inFileList):
    global pic303
    global uploadFlag
    global picLinkList
    global fileList
    uploadFlag=inUploadFlag
    picLinkList=[]
    fileList=inFileList
    if(uploadFlag==2):
        userName=input('输入pic303用户名：')
        passwd=input('输入pic303密码：')
        pic303.login(userName,passwd)
    th=[]
    for i in range(10):
        t = uploadThread(i, "Thread-%d" %i)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    return picLinkList




if __name__=='__main__':
        userName=input('输入pic303用户名：')
        passwd=input('输入pic303密码：')
        if(pic303.login(userName,passwd)):
            print(pic303.upload(r'tmp/4.jpg'))
