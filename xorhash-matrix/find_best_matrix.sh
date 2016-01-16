#!/bin/bash
# patt-matching.sh
for i in $( ls ); do

	if [ "cisco" = ${i:0:5} ]; then

		MSIZE=${i:16:${#i}}
		echo $i
		python find_best_matrix.py $i $MSIZE".out" $MSIZE

	fi
done
exit 0