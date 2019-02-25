#coding=utf-8
'''
图片来源，目前就放了xgmn5一个网站
传入文章链接，返回所有图片链接，有些网站需要指定referer的，后期再调整
'''

from xgmn5Single import getxgmn5AlbumPicLinkAndTitle

def getPicLinkAndTitle(url):
    if url.find('xgmn5')!=-1:
        return getxgmn5AlbumPicLinkAndTitle(url)
