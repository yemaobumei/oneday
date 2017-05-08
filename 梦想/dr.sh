#!/bin/sh

for k in $(seq 1 1000)
do
	phantomjs dream.js
	sleep 0.02
done
