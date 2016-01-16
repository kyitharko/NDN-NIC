#!/bin/bash

if [ $# -gt 0 ]; then
	NAME=$1
	#echo $NAME
	
	PREFIX=${NAME:0:17}
	#echo $PREFIX

	COUNTER=12
	BASE=2
	while [ $COUNTER -lt 20 ]; do
		let COUNTER=COUNTER+1
		MSIZE=$((2**$COUNTER))

		echo "python $NAME $PREFIX$MSIZE $MSIZE"
	done
	
else
	echo "Usage file_generator.sh <inFile>"
fi