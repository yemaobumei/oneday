#!/bin/bash
#获取本脚本运行pid
pid=$$
name=`basename $0`
ps -ef|grep $name|awk -v p=$pid '$2!=p {print$2}'|xargs kill -9                               
while true
do

	ps -ef|grep 'python3'|grep 'fengbao'|awk '{print$2}'|xargs kill -9 && echo  `date`
	for py in fengbao*.py
	do
		nohup python3 $py > "${py}.out" 2>&1 &
	done
	sleep 30m 
done

