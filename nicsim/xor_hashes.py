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
This module defines XOR hash function

ref paper: DEEP PACKET INSPECTION USING PARALLEL BLOOM FILTERS
"""
import random

class XorHash:
    """
    Defines an XOR-based hash function.

    Reference: M. Ramakrishna, E. Fu, and E. Bahcekapili,
    "A Performance Study of Hashing Functions for Hardware Applications,"
    Proc. 6th Int'l Conf. Computing and Information, 1994
    """
    BITMASKS = [ 1<<bit for bit in range(8) ]

    def __init__(self, vector):
        """
        Construct an XOR-based hash function.

        :param vector list of pre-determined random numbers
        """
        self.vector = vector

    def __repr__(self):
        return "XorHash(%s)" % self.vector

    def __call__(self, s):
        """
        Compute hash value.

        :param str s: input string
        :return a hash value
        :rtype int
        """
        h = 0
        j = 0

        for char in s:
            c = ord(char)
            for bit in self.BITMASKS:
                if bit & c != 0:
                    h ^= self.vector[j]
                j += 1

        return h

    @staticmethod
    def create(m, maxInputSize=500):
        """
        Create a random XorHash.

        :param int m: exclusive upper bound of hash value; should be power of 2
        :param int maxInputSize: maximum size of input this hash function can accomodate
        """
        import random
        vector = [ random.randint(0, m-1) for j in range(maxInputSize * 8) ]
        return XorHash(vector)

class XorHashes:
    """
    Defines a group of XOR-based hash functions.
    """
    def __init__(self, vectors):
        """
        Construct a group of XOR-based hash functions.

        :param vectors list of term vectors
        """
        self.functions = [ XorHash(vector) for vector in vectors ]

    def __repr__(self):
        return 'XorHashes(%s)' % [ f.vector for f in self.functions ]

    def __call__(self, s):
        """
        Compute hash values.

        :param str s: input string
        :return hash values
        :rtype list of int
        """
        return [ f(s) for f in self.functions ]

    @staticmethod
    def create(nFunctions, m, maxInputSize=500):
        """
        Create a group of random XorHashes.

        :param int nFunctions: number of hash functions
        :param int m: exclusive upper bound of hash value; should be power of 2
        :param int maxInputSize: maximum size of input hash functions can accomodate
        """
        xhs = XorHashes([])
        xhs.functions = [ XorHash.create(m, maxInputSize) for i in range(nFunctions) ]
        return xhs

if __name__ == "__main__":
    TEST_INPUTS = ["/A/1", "/A/2", "/B/1", "/B/2"]

    print "Random hash vectors."
    xhs = XorHashes.create(3, 1<<16)
    for INPUT in TEST_INPUTS:
        print INPUT, xhs(INPUT)

    print "Fixed hash vectors."
    xhs1 = XorHashes([list(range(0, 200)), list(range(200, 400)), list(range(400, 600)), list(range(600, 800))])
    xhs2 = XorHashes([list(range(0, 200)), list(range(200, 400)), list(range(400, 600)), list(range(600, 800))])
    for INPUT in TEST_INPUTS:
        print INPUT, xhs1(INPUT), xhs2(INPUT)
