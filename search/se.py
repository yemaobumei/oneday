#encoding=utf-8
import os
import re
import sys

#查找是否还有某个文件
def get_file(path,name):
	files=os.listdir(path)#列出当前所有文件／目录
	file_path=[]
	for fi in files:
		fi_path=path+'/'+fi #单个文件的完整路径名
		if os.path.isfile(fi_path):
			if name in fi:
				file_path.append(fi_path)
		elif(os.path.isdir(fi_path)):
			file_path+=get_file(fi_path,name)
	return file_path

#查找某个文件夹
def get_dir(path,name):
	files=os.listdir(path)#列出当前所有文件／目录
	file_path=[]
	for fi in files:
		fi_path=path+'/'+fi #单个文件的完整路径名
		if(os.path.isdir(fi_path)):
			if name in fi:
				file_path.append(fi_path)
			else:
				file_path+=get_dir(fi_path,name)
	return file_path


if __name__=='__main__':
	paths=sys.path
	name='six.py'
	f_path=[]
	for path in paths:
		try:
			f_path+=get_file(path,name)
		except OSError:
			f_path=f_path
	print f_path