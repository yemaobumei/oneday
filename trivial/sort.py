def div(lst):
	left=[]
	right=[]
	mid=[]
	if len(lst)==0:
		return []
	for each_num in lst:
		if each_num<lst[0]:
			left.append(each_num)
		elif each_num>lst[0]:
			right.append(each_num)
		else:
			mid.append(each_num)

	if len(left)<=1 and len(right)<=1:
		return left+mid+right
	else:
		return div(left)+mid+div(right)


class Solution(object):
	def __init__(self,lst):
		self.lst=lst

	def quick_sort(self,l,r):
		if l>=r:return
		i=l
		j=r
		pivot=self.lst[i]
		while i<j:
			while i<j and self.lst[i]>=self.lst[j]:
				j-=1
			if i<j:
				self.lst[i]=self.lst[j]
				i+=1
			while i<j and self.lst[i]<=pivot:
				i+=1
			if i<j:
				self.lst[j]=self.lst[i]
				j-=1
		self.lst[i]=pivot
		self.quick_sort(l,i-1)
		self.quick_sort(i+1,r)

import random
a=[random.randint(1,10) for i in range(10)]
b=Solution(a)

