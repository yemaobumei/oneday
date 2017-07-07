#!/bin/sh
while true
do
	for py in fengbao*.py
	do
		nohup python3 $py > "${py}.out" 2>&1 &
	done
#	nohup python3 fengbao.py >fengbao.out 2>&1 &
	sleep 30m && ps -ef|grep 'python3'|grep 'fengbao'|awk '{print$2}'|xargs kill -9 && echo -e `date`
done

