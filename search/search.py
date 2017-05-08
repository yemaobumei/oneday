# -*- coding: utf-8 -*-
#查找某个文本内容里还有某字段

#list all the files in your path(完整路径名path\**.py)
import os
import re
def get_files(path):
    files=os.listdir(path)#列出所有文件
    files_path=[]
    for fi in files:
        fi_path= path+'/' + fi#单个文件路径
        if os.path.isfile(fi_path):
            if fi.split('.')[-1]=='py':
                files_path.append(fi_path)
        elif(os.path.isdir(fi_path)):
            files_path+=get_files(fi_path)
    return files_path

def search(files):
    find_file=[]
    for filename in files:
        f = open(filename, 'rb')
        for l in f:
            l = l.strip()
            m=re.match('CharField|FieldFile',l)
	    if m is not None:
               find_file.append(filename)
               break
        f.close()
    return find_file

if __name__ == '__main__':
    a=r'c:\python27'
    files = get_files(r'/usr/local/lib/python2.7/dist-packages/django/db/models')
    #files = get_files(r'F\v6:')
    print search(files)
