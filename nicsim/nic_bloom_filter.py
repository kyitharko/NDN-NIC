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

from xor_hashes import XorHashes

class NicBloomFilter:
    """
    Bloom filter for NDN-NIC simulator.
    This differs from a regular Bloom filter in that:
    (1) keys are remembered in a table, so that NicBloomFilter can determine
        whether a match in the regular Bloom filter is a false positive.
    (2) each key is associated with one or more reason codes.

    :param int mBuckets: number of buckets
    """
    def __init__(self, mBuckets):
        self.mBuckets = mBuckets
        self.buckets = [0] * mBuckets
        self.table = dict()
        # default 3 hash functions
        self.xorHashes = XorHashes.create(3, mBuckets)

    def add(self, key, reasonCode):
        """
        Add a key to the counting bloom filter
        Add (key, [reasonCode]) to the table (Append the list)

        :param string key: Uri format of name with "/"
        :param string reasonCode: the reason to insert the key (e.g., PIT, FIB, CS, etc.)
        """
        hashes = self.xorHashes(key)
        for h in hashes:
            self.buckets[h % self.mBuckets] += 1

        self.table.setdefault(key, []).append(reasonCode)

    def remove(self, key, reasonCode):
        """
        Remove a key from the counting bloom filter
        Remove (key, [reasonCode]) from the table

        :param string key
        :param string reasonCode: the reason to insert the key
        """
        if key not in self.table.keys():
            raise KeyError

        self.table[key].remove(reasonCode)
        if len(self.table[key]) == 0:
            self.table.pop(key)

        hashes = self.xorHashes(key)
        for h in hashes:
            self.buckets[h % self.mBuckets] -= 1

    def query(self, key):
        """
        Query whether the key is in bloom filter and check if it is a false positive.

        :param string key
        :return: list of reasonCodes, False, or "FP"
        """
        hashes = self.xorHashes(key)

        for h in hashes:
            if self.buckets[h % self.mBuckets] == 0:
                return False

        return self.table.get(key, "FP")

    def __str__(self):
        return "Bloom Filter buckets: %s\nBloom Filter table: %s\n" % (self.buckets, self.table)
