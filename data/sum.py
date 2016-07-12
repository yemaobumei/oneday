#encoding=utf-8
import os
import re

#获取文件数据
def get_data(path):
	files=os.listdir(path)#列出所有文件
	arr=[]#存储第二列至第五列数据
	first=[]#存储第一列数据
	for file in files:
		file=path+'/'+file
		if os.path.isfile(file) and file.split('.')[-1]=='cluster':
			f=open(file,'rb')
			while True:
				line=f.readline()
				if not line:
					break
				line=line.strip()
				line=re.split(r'\s+',line)
				line_datas=map(int,line)
				arr.append(line_datas[1:])
				first.append(line_datas[0])
			f.close()
	return first,arr

#比较arr数据是否相同,分类统计
def analyse_data(first,arr):
	a=[]#去重化数组
	for each in arr:
		if each not in a:
			a.append(each)
	b=[0]*(len(a))#用来记录不同类的数据
	for i,j in enumerate(a):		
		for index,element in enumerate(arr):
			if element==j:
				b[i]+=first[index]
	return a,b


			



if __name__ == '__main__':
	path=r"/Users/yefan/Desktop/data"
	index,arr=get_data(path)
	a,b=analyse_data(index,arr)
	result=open(path+'/'+'result.txt','wb')
	for i,j in enumerate(a):
		result.write(str(j)+'  ')
		result.write(str(b[i])+'\n')
	result.close()
	
