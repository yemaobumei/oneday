#encoding=utf-8
#一行实现寻找素数。
filter(lambda x:all([x%i for i in range(2,x)]),range(2,100))
[x for x in range(2,100) if all([x%i for i in range(2,x)])]

