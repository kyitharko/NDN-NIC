import sys

if len(sys.argv) < 2:
	print "Usage line_counter.py <file-name>"
else:
	fileName = sys.argv[1]
	inFile = open(fileName,"r")
	c = 0
	for eachLine in inFile:
		c+=1

	print "The total lines are: ",c