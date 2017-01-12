#!/bin/sh

for k in $(seq 1 100)
do
	phantomjs dream.js
	sleep 0.01
done
