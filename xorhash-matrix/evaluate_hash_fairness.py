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


"""
Evaluate the fairness for XorHashes

:param int n: the number of items inserted
:param list bucketList: a list of buckets contains the hit number of each bucket
:return: result
:rtype: float
"""
def hashFairness(n, bucketList):
    total = 0
    m = len(bucketList)

    for bucket in bucketList:
        total += bucket * bucket

    return n * n * 1.0 / m / total


from hash_function import XorHash

if __name__ == '__main__':
    xorHash = XorHash.create(128)
    buckets = [0] * 128
    for i in range(128):
        h = xorHash(str(i))
        #print h
        buckets[h] += 1

    print hashFairness(128, buckets)
