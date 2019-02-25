#coding=utf-8
'''
将写真网站中的图片上传到自己wordpress网站中
'''
import os
from picsource import getPicLinkAndTitle
from wp import wpcontent
from tuchuang import upload
from downloadPic import downdloadPics

ifUpload=True

if(os.path.exists('tmp')==False):
    os.makedirs('tmp')
userName=input('输入wordpress用户名：')
passwd=input('输入wordpress密码：')
_wp=wpcontent(userName,passwd)
x=''
a=''
title=''
while(1):
    x=input('输入链接：')
    if(x.find('xgmn5')==-1):
        continue
    a=getPicLinkAndTitle(x)
    title=a.pop()
    if(ifUpload):
        fileList=downdloadPics(a)
        fileList.reverse()
        picLinkList=upload(2,fileList)
        _wp.post(title,picLinkList)
    else:
        _wp.post(title,a)
