#!/bin/sh

for k in $(seq 1 1000)
do
	phantomjs dream2.js
	sleep 0.02
done
