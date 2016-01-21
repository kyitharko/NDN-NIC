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

class HmacHash:
    """
    Provides a hash function based on hmac module.
    """
    def __init__(self, m, key, algo='sha1'):
        """
        Constructor.

        :param int m: exclusive upper bound of hash value; should be power of 2
        :param str key: HMAC key
        :param str algo: hash algorithm; must exist in hashlib
        """
        self.m = m
        self.key = key
        import hashlib
        self.digest = getattr(hashlib, algo)

    def __call__(self, s):
        """
        Compute hash value.

        :param str s: input string
        :return a hash value
        :rtype int
        """
        import hmac
        hm = hmac.new(self.key, s, self.digest)
        d = hm.digest()

        h = 0
        for char in d:
            h = (h << 8) | ord(char)

        return h % self.m

    @staticmethod
    def create(m, algo='sha1'):
        """
        Create a random HmacHash.

        :param int m: exclusive upper bound of hash value; should be power of 2
        :param str algo: hash algorithm; must exist in hashlib
        """
        import random
        key = ''.join([ chr(random.randrange(256)) for i in range(16) ])
        return HmacHash(m, key, algo)

def __load_cXorHash():
    import os
    sopath = os.path.join(os.path.dirname(__file__), "../xorhash-c/lib/python/xorhash.so")
    import imp
    try:
        xorhash = imp.load_dynamic("xorhash", sopath)
    except ImportError:
        return None
    return xorhash.XorHash
cXorHash = __load_cXorHash()

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
        self.cHasher = None if cXorHash is None else cXorHash(vector)

    def __repr__(self):
        return "XorHash(%s)" % self.vector

    def __call__(self, s):
        """
        Compute hash value.

        :param str s: input string
        :return a hash value
        :rtype int
        """
        if self.cHasher is not None:
            return self.cHasher(s)

        h = 0
        j = 0
        if len(s) * 8 > len(self.vector):
            raise IndexError("input is too long for vector")

        for char in s:
            c = ord(char)
            for bit in self.BITMASKS:
                if bit & c != 0:
                    h ^= self.vector[j]
                j += 1

        return h

    @staticmethod
    def create(m, maxInputSize=4096, polyFile=None):
        """
        Create a random XorHash.

        :param int m: exclusive upper bound of hash value; should be power of 2
        :param int maxInputSize: maximum size of input this hash function can accomodate
        """
        if polyFile is None:
            with open("/dev/urandom", "r") as f:
                return XorHash.create(m, maxInputSize, f)

        import struct
        vectorStruct = struct.Struct("!%dQ" % (maxInputSize * 8))
        vector = [ (x % m) for x in vectorStruct.unpack(polyFile.read(vectorStruct.size)) ]
        return XorHash(vector)

class HashGroup:
    """
    A function to compute multiple hashes on the same input.
    """
    def __init__(self, functions):
        self.functions = functions

    def __call__(self, s):
        """
        Compute hash values.

        :param str s: input string
        :return hash values
        :rtype list of int
        """
        return [ f(s) for f in self.functions ]

    def __len__(self):
        return len(self.functions)

if __name__ == "__main__":
    print "cXorHash is %s" % ("missing" if cXorHash is None else "available")

    TEST_INPUTS = ["/A/1", "/A/2", "/B/1", "/B/2"]

    hg = HashGroup([
      HmacHash(1<<16, "key"),
      HmacHash.create(1<<16),
      XorHash(range(16000, 16200)),
      XorHash.create(1<<16),
    ])

    for INPUT in TEST_INPUTS:
        print INPUT, hg(INPUT)
