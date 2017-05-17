#!/bin/sh
nohup python3 fengbao.py >fengbao.out &
while true
do
	
	sleep 20m && ps -ef|grep 'python3'|grep 'fengbao'|awk '{print$2}'|xargs kill -9 && nohup python3 fengbao.py >fengbao.out &
done

