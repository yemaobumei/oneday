#!/usr/bin/env python
#encoding=utf-8
"""
读取某目录下所有文件名，然后携程img格式插入到html文档中。
"""


import re, requests,os

SAVE_DIR_PATH = r'/home/alien/pic/'
div1="<div class=\"wrap\">\n"+"	"+"<div class=\"in\">\n"
div2='	'+"</div>\n"+"</div>\n"
URL = 'http://www.zhihu.com/question/37006507'
f=open(SAVE_DIR_PATH+"img.html", 'wb');
save = lambda url: f.write(div1+"		"+"<img src=\""+"{%static 'images/pic/"+url+"'%}\""+">"+'\n'+div2)

if __name__ == '__main__':
	map(save,os.listdir(SAVE_DIR_PATH))