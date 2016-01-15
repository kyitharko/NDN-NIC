import sys

if len(sys.argv) < 4:
	print "Usage file_generator.py <in-file> <out-file> <line-number>"
else:
	inFileName = sys.argv[1]
	outFileName = sys.argv[2]
	n = int(sys.argv[3])

	inFile = open(inFileName,"r")
	outFile = open(outFileName,"w")

	c = 0
	for eachLine in inFile:
		outFile.writelines(eachLine)
		c+=1
		if c >= n:
			break

	print "The total lines are: ",c
	inFile.close()
	outFile.close()