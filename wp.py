#coding=utf-8
'''
上传图片链接以及标题到自己wordpress网站中
使用了插件Featured Image From URL
'''
import requests
import re
import time
import datetime

#site填写自己的网站http开头，末尾不带斜杠
site=''
loginurl=site+'/wp-login.php'
#categoryUrl可以读取网站中的所有分类，这里直接指定了，就不用读取了
categoryUrl=site+'/wp-admin/edit-tags.php?taxonomy=category'
#categoryID为文章的分类序号
categoryID='13'
postNewUrl=site+'/wp-admin/post-new.php'
postUrl=site+'/wp-admin/post.php'
header = {
    "Referer": site+'/wp-admin/post-new.php',
}

class wpcontent:
    s=requests.session()
    _wpnonce=''
    post_ID=''
    meta_box_order_nonce=''
    closedpostboxesnonce=''
    samplepermalinknonce=''
    _ajax_nonceaddcategory=''
    _ajax_nonceaddmeta=''
    def __init__(self,userName,passwd): #初始化登录
        loginPostData={'log':userName,'pwd':passwd,'wp-submit':'%E7%99%BB%E5%BD%95','redirect_to':site+'/wp-admin/'}
        response=self.s.post(loginurl,data=loginPostData)
        print("login")

    def __getPostInfo(self):
        response=self.s.get(postNewUrl)
        reg=r'_wpnonce" value="(.*?)"'
        tmpre=re.compile(reg)
        self._wpnonce=tmpre.findall(response.text)[0]
        reg=r"post_ID' value='(.*?)'"
        tmpre=re.compile(reg)
        self.post_ID=tmpre.findall(response.text)[0]
        reg=r'meta-box-order-nonce" value="(.*?)"'
        tmpre=re.compile(reg)
        self.meta_box_order_nonce=tmpre.findall(response.text)[0]
        reg=r'closedpostboxesnonce" value="(.*?)"'
        tmpre=re.compile(reg)
        self.closedpostboxesnonce=tmpre.findall(response.text)[0]
        reg=r'samplepermalinknonce" value="(.*?)"'
        tmpre=re.compile(reg)
        self.samplepermalinknonce=tmpre.findall(response.text)[0]
        reg=r'ajax_nonce-add-category" value="(.*?)"'
        tmpre=re.compile(reg)
        self._ajax_nonceaddcategory=tmpre.findall(response.text)[0]
        reg=r'ajax_nonce-add-meta" value="(.*?)"'
        tmpre=re.compile(reg)
        self._ajax_nonceaddmeta=tmpre.findall(response.text)[0]
        print(self.post_ID)

    def __picLink2html(self,picLinkList):
        html=''
        for x in picLinkList:
            html=html+'<img src="'+x+'" />'
        return html

    def post(self,title,picLinkList):
        self.__getPostInfo()
        content=self.__picLink2html(picLinkList)
        postData={"_wpnonce":self._wpnonce,
            "_wp_http_referer":"/wp-admin/post-new.php",
            "user_ID":"1",
            "action":"editpost",
            "post_author":"1",
            "post_type":"post",
            "original_post_status":"auto-draft",
            "referredby":site+"/wp-admin/edit.php",
            "_wp_original_http_referer":site+"/wp-admin/edit.php",
            "auto_draft":"1",
            "post_ID":self.post_ID,
            "meta-box-order-nonce":self.meta_box_order_nonce,
            "closedpostboxesnonce":self.closedpostboxesnonce,
            "post_title":title,
            "samplepermalinknonce":self.samplepermalinknonce,
            "content":content,
            "wp-preview":"",
            "hidden_post_status":"draft",
            "post_status":"draft",
            "hidden_post_password":"",
            "hidden_post_visibility":"public",
            "post_password":"",
            "aa":str(datetime.date.today().year),
            "mm":str(datetime.date.today().month),
            "jj":str(datetime.date.today().day),
            "hh":str(time.strftime('%H',time.localtime())),
            "mn":str(time.strftime('%M',time.localtime())),
            "ss":str(time.strftime('%S',time.localtime())),
            "hidden_mm":str(datetime.date.today().month),
            "cur_mm":str(datetime.date.today().month),
            "hidden_jj":str(datetime.date.today().day),
            "cur_jj":str(datetime.date.today().day),
            "hidden_aa":str(datetime.date.today().year),
            "cur_aa":str(datetime.date.today().year),
            "hidden_hh":str(time.strftime('%H',time.localtime())),
            "cur_hh":str(time.strftime('%H',time.localtime())),
            "hidden_mn":str(time.strftime('%M',time.localtime())),
            "cur_mn":str(time.strftime('%M',time.localtime())),
            "original_publish":"%E5%8F%91%E5%B8%83",
            "publish":"%E5%8F%91%E5%B8%83",
            "post_format":"0",
            "post_category[]":categoryID,
            "newcategory":"%E6%96%B0%E5%88%86%E7%B1%BB%E7%9B%AE%E5%BD%95%E5%90%8D",
            "newcategory_parent":"-1",
            "_ajax_nonce-add-category":self._ajax_nonceaddcategory,
            "tax_input[post_tag]":"",
            "newtag[post_tag]":"",
            "_thumbnail_id":"-1",
            "fifu_input_alt":"",
            "fifu_input_url":picLinkList[0],
            "excerpt":"",
            "trackback_url":"",
            "metakeyselect":"#NONE#",
            "metakeyinput":"",
            "metavalue":"",
            "_ajax_nonce-add-meta":self._ajax_nonceaddmeta,
            "advanced_view":"1",
            "comment_status":"open",
            "ping_status":"open",
            "post_name":"",
            "post_author_override":"1"
        }
        response=self.s.post(postUrl,data=postData,headers=header)
        print(title+'   post')
