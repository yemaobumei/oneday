#!/bin/sh
while true
do
	python3 fengbao.py
	sleep 30m && ps -ef|grep 'python3'|grep 'fengbao'|awk '{print$2}'|xargs kill -9
done

