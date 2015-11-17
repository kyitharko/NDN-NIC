def computeHashes(key):
    return [1]


"""
This module defines simulation of NIC bloom filter
"""

class NicBloomFilter:
    """
    Create a new NIC bloom filter which contains both a counting bloom filter (list)
    and a table (directory)
    """

    def __init__(self, mBuckets):
        self.buckets = [0] * mBuckets
        self.table = dict()

    def add(self, key, reasonCode):
        """
        Add a key to the counting bloom filter
        Add (key, [reasonCode]) to the table (Append the list)

        :param string key: Uri format of name with "/"
        :param string reasonCode: the reason to insert the key (e.g., PIT, FIB, CS, etc.)
        """
        # key is in Uri format
        hashes = computeHashes(key)
        for eachHash in hashes:
            self.buckets[eachHash] += 1
        
        if key in self.table.keys():
            self.table[key].append(reasonCode)
        else:
            self.table[key] = [reasonCode]

    def remove(self, key, reasonCode):
        """
        Remove a key from the counting bloom filter
        Remove (key, [reasonCode]) from the table

        :param string key: Uri format of name with "/"
        :param string reasonCode: the reason to insert the key (e.g., PIT, FIB, CS, etc.)
        """
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
        """
        Query whether the key is in bloom filter and check if it is a FP
        by checking the table

        :param string key: Uri format of name with "/"
        :return: True, False or "FP"
        :rtype: bool or string
        """
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