# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2015-2016 Arizona Board of Regents
# Author: Teng Liang <philoliang@email.arizona.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# A copy of the GNU Lesser General Public License is in the file COPYING.

class NicBloomFilter:
    """
    Bloom filter for NDN-NIC simulator.

    This extends a regular Bloom filter:
    (1) Keys are recorded in a table, so that NicBloomFilter can determine
        whether a match in the regular Bloom filter is a false positive.
    (2) Each key is associated with one or more reason codes.
    """
    @staticmethod
    def __makeHasher(hasher, m):
        from hash_function import HashGroup, HmacHash
        if isinstance(hasher, HashGroup):
            return hasher
        elif isinstance(hasher, (int, long)):
            return HashGroup([ HmacHash.create(m) for i in range(hasher) ])
        elif hasher is None:
            return NicBloomFilter.__makeHasher(3, m)
        else:
            raise TypeError("unexpected type for Bloom filter")

    def __init__(self, m, hasher=None):
        """
        Constructor.

        :param int m: number of buckets
        :param hasher: a HashGroup that computes a vector of hashes in [0,m) range for a key,
                       or an int to create a HashGroup with that many random HmacHash functions,
                       or None to create a HashGroup with 3 random HmacHash functions
        """
        self.m = m
        self.buckets = [0] * m
        self.table = dict()
        self.hasher = NicBloomFilter.__makeHasher(hasher, m)
        self.isUpdating = False

    def __len__(self):
        return len(self.table)

    def add(self, key, reasonCode):
        """
        Add a key with a reason code

        :param string key: Uri format of name with "/"
        :param string reasonCode: a reason code; may repeat
        """
        assert self.isUpdating
        self.table.setdefault(key, []).append(reasonCode)

        hashes = self.hasher(key)
        for h in hashes:
            if self.buckets[h] == 0:
                self.clearBits.discard(h)
                self.setBits.add(h)
            self.buckets[h] += 1

    def remove(self, key, reasonCode):
        """
        Remove a key with a reason code

        :param string key
        :param string reasonCode: the reason to insert the key
        """
        assert self.isUpdating
        if key not in self.table:
            raise KeyError

        reasonCodes = self.table[key]
        reasonCodes.remove(reasonCode)
        if len(reasonCodes) == 0:
            self.table.pop(key)

        hashes = self.hasher(key)
        for h in hashes:
            self.buckets[h] -= 1
            if self.buckets[h] == 0:
                self.setBits.discard(h)
                self.clearBits.add(h)

    def beginUpdate(self):
        """
        Begin a series of updates.
        """
        assert not self.isUpdating
        self.isUpdating = True
        self.setBits = set()
        self.clearBits = set()

    def endUpdate(self):
        """
        Commit a series of updates.

        :return (int, int) count of hardware bits with 0-to-1 and 1-to-0 transitions
        """
        assert self.isUpdating
        self.isUpdating = False
        return (len(self.setBits), len(self.clearBits))

    def query(self, key):
        """
        Lookup a key with its reason codes

        :param string key
        :return list of reasonCodes if key exists, False if key does not exist,
                or "FP" if key exists in Bloom filter due to false positive
        """
        hashes = self.hasher(key)
        if not all([self.buckets[h] for h in hashes]):
            return False

        return self.table.get(key, "FP")

    def capacity(self, maxFp=1.0):
        """
        Compute the capacity given upper bound of false positive probability.

        :param float maxFp: upper bound of false positive probability
        :return capacity
        :rtype float
        """
        # classic formula: f = (1-e^(-(n k)/m))^k
        # inverse function: n = -(m log(1-f^(1/k)))/k
        import math
        k = len(self.hasher)
        return -(self.m * math.log(1.0 - math.pow(maxFp, (1.0 / k)))) / k

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate Bloom filter false positive.")
    parser.add_argument("--k", type=int, default=3,
                        help="number of hash functions")
    parser.add_argument("--m", type=int, default=128,
                        help="number of buckets")
    parser.add_argument("--n", type=int, default=32,
                        help="number of keys")
    parser.add_argument("--t", type=int, default=1024,
                        help="number of trials")
    parser.add_argument("--keys", type=argparse.FileType('r'),
                        help="text file to read keys from; must have at least n+t lines and they must be unique")
    parser.add_argument("-v", action="store_true",
                        help="verbose output")
    args = parser.parse_args()

    if args.keys is None:
        def numericKeySource():
            i = 0
            while True:
                yield str(i)
                i += 1
        keySource = numericKeySource().__iter__()
    else:
        keySource = args.keys

    nbf = NicBloomFilter(args.m, args.k)
    nbf.beginUpdate()
    for i in range(args.n):
        key = next(keySource).rstrip()
        nbf.add(key, "X")
        if args.v:
            print "Insert key %s" % key
    (setBits, clearedBits) = nbf.endUpdate()
    print "%d bits set" % setBits
    assert clearedBits == 0

    nFalsePositives = 0
    import random
    for i in range(args.t):
        key = next(keySource).rstrip()
        result = nbf.query(key)
        if args.v:
            print "Lookup key %s %s" % (key, "OK" if result is False else "FP")
        if result == "FP":
            nFalsePositives += 1

    fpRateActual = float(nFalsePositives) / args.t
    capacityFpActual = nbf.capacity(fpRateActual)

    import math
    fpRate1 = math.pow(1 - math.exp(-float(args.n) * args.k / args.m), args.k)
    kOpt = float(args.m) / args.n * math.log(2)
    fpRate1kOpt = math.pow(1 - math.exp(-float(args.n) * kOpt / args.m), kOpt)

    print "Actual FP rate = %0.6f" % fpRateActual
    print "Capacity for actual FP rate = %0.6f" % capacityFpActual
    print "FP probability (classic formula) = %0.6f" % fpRate1
    print "Optimal k = %0.6f" % kOpt
    print "FP rate with optimal k = %0.6f" % fpRate1kOpt
