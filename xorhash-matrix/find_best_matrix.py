from hash_function import XorHash
from evaluate_hash_fairness import hashFairness
import sys

if len(sys.argv) < 4:
    print "Usage: python find_best_matrix.py [<input_file>] [<output_file>] [<m>]"
else:
    inFileName = sys.argv[1]
    outFileName = sys.argv[2]
    m = int(sys.argv[3])
    inFile = open(inFileName,'r')
    outFile = open(outFileName,'w')

    xorHashList = [XorHash.create(m) for i in range(500)]
    outList = []
    #m = 1<<20 

    j = 0
    for eachHash in xorHashList:
        j+=1
        print j

        buckets = [0] * m
        c = 0
        for eachLine in inFile:
            c += 1
            h = eachHash(eachLine) 
            buckets[h] += 1
        inFile.seek(0)

        fairness = hashFairness(c, buckets)
        #uncomment the next line for random parameters
        #outList.append((eachHash,fairness))

        outList.append(fairness)

    #outList = sorted(outList,reverse=True, key=lambda k : k[1])
    outList = sorted(outList)
    outList = [str(i) for i in outList]

    #print outList
    """
    for eachTuple in outList:
        #print eachTuple[1]
        #print type(eachTuple[0])
        vector =  " ".join([str(i) for i in eachTuple[0].vector])
        outFile.writelines(str(eachTuple[1])+"\t"+vector+'\n')
    """
    outFile.writelines("\n".join(outList))

    inFile.close()
    outFile.close()