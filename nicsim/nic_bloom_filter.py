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
    (1) keys are records in a table, so that NicBloomFilter can determine
        whether a match in the regular Bloom filter is a false positive.
    (2) each key is associated with one or more reason codes.

    :param int m: number of buckets
    :param hasher: a function that computes a vector of hashes in [0,m) range for a key
    """
    def __init__(self, m, hasher=None):
        self.m = m
        self.buckets = [0] * m
        self.table = dict()
        if hasher is None:
            from xor_hashes import XorHashes
            self.hasher = XorHashes.create(3, m)
        else:
            self.hasher = hasher

    def add(self, key, reasonCode):
        """
        Add a key with a reason code

        :param string key: Uri format of name with "/"
        :param string reasonCode: a reason code; may repeat
        """
        self.table.setdefault(key, []).append(reasonCode)

        hashes = self.hasher(key)
        for h in hashes:
            self.buckets[h] += 1

    def remove(self, key, reasonCode):
        """
        Remove a key with a reason code

        :param string key
        :param string reasonCode: the reason to insert the key
        """
        if key not in self.table:
            raise KeyError

        reasonCodes = self.table[key]
        reasonCodes.remove(reasonCode)
        if len(reasonCodes) == 0:
            self.table.pop(key)

        hashes = self.hasher(key)
        for h in hashes:
            self.buckets[h] -= 1

    def query(self, key):
        """
        Lookup a key with its reason codes

        :param string key
        :return: list of reasonCodes if key exists, False if key does not exist,
                 or "FP" if key exists in Bloom filter due to false positive
        """
        hashes = self.hasher(key)
        if not all([self.buckets[h] for h in hashes]):
            return False

        return self.table.get(key, "FP")
