#!/bin/bash
#获取本脚本运行pid
pid=$$
name=`basename $0`
ps -ef|grep $name|awk -v p=$pid '$2!=p {print$2}'|xargs kill -9                               
while true
do
	ps -ef|grep 'python3'|grep 'DanmuClient'|awk '{print$2}'|xargs kill -9 && echo  `date`
	python3 getTopUp.py
	nohup python3 DanmuClientManager.py &
	sleep 30m 
done

