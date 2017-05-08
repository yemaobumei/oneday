#!/usr/bin/env python
#encoding=utf-8
"""

爬取网页上的图片地址，然后写成html中img格式，可以批量将图片插入已知的html文档。（前提是先将网页上的图片下载下来存放到pic下）
"""


import re, requests

SAVE_DIR_PATH = r'/home/alien/pic/'
div1="<div class=\"wrap\">\n"+"	"+"<div class=\"in\">\n"
div2='	'+"</div>\n"+"</div>\n"
URL = 'http://www.zhihu.com/question/37006507'
f=open(SAVE_DIR_PATH+"img.html", 'wb');
save = lambda url: f.write(div1+"		"+"<img src=\""+"{%static 'images/pic/"+url[url.rfind('/')+1:]+"'%}\""+">"+'\n'+div2)

if __name__ == '__main__':
    map(save, [url[1] for url in re.findall(ur'(<img.*?src=["])(https://pic.+?)(["].+?jpg">)', requests.get(URL,verify=False).content)])
#    open(r'c:\python27\oneday_one\list.txt','w').write(requests.get(URL).content)