#!/bin/sh
while true
do
	nohup python3 ningmengfengbao.py >fengbao.out 2>&1 &
	sleep 30m && ps -ef|grep 'python3'|grep 'ningmengfengbao'|awk '{print$2}'|xargs kill -9 && echo -e `date`
done

