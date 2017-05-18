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

import unittest as ut
from nic_bloom_filter import NicBloomFilter

class NicBloomFilterTestCase(ut.TestCase):
    def setUp(self):
        self.nbf = NicBloomFilter(128)
        self.nbf.beginUpdate()

    def test_simple(self):
        self.assertEqual(len(self.nbf), 0)
        self.nbf.add("/A", "PIT1")
        self.assertEqual(len(self.nbf), 1)
        self.nbf.add("/C/1", "PIT1")
        self.assertEqual(len(self.nbf), 2)
        self.nbf.add("/C/1", "PIT1")
        self.assertEqual(len(self.nbf), 2)
        self.assertEqual(self.nbf.query("/A"), ["PIT1"])
        self.assertEqual(self.nbf.query("/B"), False)
        self.assertEqual(self.nbf.query("/C/1"), ["PIT1", "PIT1"])

    def test_remove(self):
        self.nbf.add("/A", "PIT1")
        self.nbf.add("/A", "PIT1")
        self.assertEqual(len(self.nbf), 1)
        self.nbf.remove("/A", "PIT1")
        self.assertEqual(len(self.nbf), 1)
        self.assertEqual(self.nbf.query("/A"), ["PIT1"])
        self.nbf.remove("/A", "PIT1")
        self.assertEqual(len(self.nbf), 0)
        self.assertEqual(self.nbf.query("/A"), False)

    def test_fp(self):
        """
        Saturate the Bloom filter,
        and lookup a diffent key expecting a false positive
        """
        for i in range(1024):
            self.nbf.add(str(i), "PIT1")
        self.assertEqual(self.nbf.query("x"), "FP")

    def test_counters(self):
        nSets, nClears = self.nbf.endUpdate()
        self.assertEquals(nSets, 0)
        self.assertEquals(nClears, 0)

        self.nbf.beginUpdate()
        self.nbf.add("/A", "FIB")
        nSets, nClears = self.nbf.endUpdate()
        self.assertGreater(nSets, 0)
        self.assertEquals(nClears, 0)

        self.nbf.beginUpdate()
        self.nbf.remove("/A", "FIB")
        nSets2, nClears2 = self.nbf.endUpdate()
        self.assertEquals(nSets2, 0)
        self.assertEquals(nClears2, nSets)

if __name__ == '__main__':
    ut.main(verbosity=2)
