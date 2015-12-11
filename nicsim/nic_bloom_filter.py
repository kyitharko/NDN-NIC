# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2015-2016 Regents of the University of Arizona
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


"""
This module defines simulation of NIC bloom filter
"""

from xor_hashes import XorHashes

class NicBloomFilter:
    """
    Create a new NIC bloom filter which contains both a counting bloom filter (list)
    , a table (directory) and a new XorHashes

    :param int mBuckets: the size of buckets
    """
    def __init__(self, mBuckets):
        self.mBuckets = mBuckets
        self.buckets = [0] * mBuckets
        self.table = dict()
        #default 3 hash functions
        self.xorHashes = XorHashes(3, mBuckets)

    def add(self, key, reasonCode):
        """
        Add a key to the counting bloom filter
        Add (key, [reasonCode]) to the table (Append the list)

        :param string key: Uri format of name with "/"
        :param string reasonCode: the reason to insert the key (e.g., PIT, FIB, CS, etc.)
        """
        # key is in Uri format
        hashes = self.xorHashes.computeHashes(key)
        for eachHash in hashes:
            self.buckets[eachHash % self.mBuckets] += 1

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
        hashes = self.xorHashes.computeHashes(key)
        for eachHash in hashes:
            self.buckets[eachHash % self.mBuckets] -= 1

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
        :return: reasonCode, False or "FP"
        :rtype: bool or string
        """
        hashes = self.xorHashes.computeHashes(key)
        isInBuckets = True

        for eachHash in hashes:
            if self.buckets[eachHash % self.mBuckets] == 0:
                isInBuckets = False
                break

        if isInBuckets:
            if key in self.table.keys():
                return self.table[key]
            else:
                return "FP"
        else:
            return False

    def __str__(self):
        return "Bloom Filter buckets: " + str(self.buckets) + "\nBloom Filter table: " + str(self.table) + '\n'
