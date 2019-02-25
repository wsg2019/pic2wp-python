# pic2wp-python
初学python，第一个项目


### pic2wp

将写真网站上的图集收集自己喜欢的，直接使用原来链接或者通过上传到图床，再发布到自己的wordpress网站上

#### picsource.py

图片来源，目前就放了xgmn5一个网站
传入文章链接，返回所有图片链接，有些网站需要指定referer的，后期再调整

##### downloadPic.py

下载传入的图片链接，保存到目录tmp下，并按序号重命名，返回文件列表

#### tuchuang.py（图床）

将相应的图片文件上传，返回图片链接
调用upload(inUploadFlag,inFileList)
第一个参数指定图床
    0：sm.ms
    1：siimg一类的
    2：chevereto一类的（pic303.com）
第二个参数指定图片文件列表

#### wp.py

上传图片链接以及标题到自己wordpress网站中
使用了插件Featured Image From URL

------

##### xgmn5Single.py

一、下载xgmn5.com中指定链接下的图片
使用如下
python xgmn5.py https://www.xgmn5.com/MiiTao/MiiTao10569.html

二、在项目pic2wp中使用获取图片链接以及标题(getPicLinkAndTitle)
