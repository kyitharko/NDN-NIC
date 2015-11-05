def computeHashes(key):
    return [1]

class NicBloomFilter:
    def __init__(self, mBuckets):
        self.buckets = [0] * mBuckets
        self.table = dict()

    def add(self, key, reasonCode):
        # key is in Uri format
        hashes = computeHashes(key)
        for eachHash in hashes:
            self.buckets[eachHash] += 1
        
        if key in self.table.keys():
            self.table[key].append(reasonCode)
        else:
            self.table[key] = [reasonCode]

    def remove(self, key, reasonCode):
        hashes = computeHashes(key)
        for eachHash in hashes:
            self.buckets[eachHash] -= 1
         
        if key not in self.table.keys():
            raise KeyError
        else:
            self.table[key].remove(reasonCode)

            if self.table[key] == []:
                self.table.pop(key)

    def query(self, key):
        hashes = computeHashes(key)
        isInBuckets = True
        
        for eachHash in hashes:
            if self.buckets[eachHash] == 0:
                isInBuckets = False
                break

        if isInBuckets:
            if key in self.table.keys():
                return self.table[key]
            else:
                return "FP"
        else:
            return False


if __name__ == "__main__":
    nicBloomFilter = NicBloomFilter(100)
    nicBloomFilter.add("/ndn","PIT")
    print nicBloomFilter.query("/ndn")
    print nicBloomFilter.query("/ua")
    nicBloomFilter.remove("/ndn","PIT")
    print nicBloomFilter.query("ndn")