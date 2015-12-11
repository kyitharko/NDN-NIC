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
        self.bf = NicBloomFilter(128)

    def test_simple(self):
        self.bf.add("/A", "PIT1")
        self.bf.add("/C/1", "PIT1")
        self.bf.add("/C/1", "PIT1")
        self.assertEqual(self.bf.query("/A"), ["PIT1"])
        self.assertEqual(self.bf.query("/B"), False)
        self.assertEqual(self.bf.query("/C/1"), ["PIT1", "PIT1"])

    def test_remove(self):
        self.bf.add("/A", "PIT1")
        self.bf.add("/A", "PIT1")
        self.bf.remove("/A", "PIT1")
        self.assertEqual(self.bf.query("/A"), ["PIT1"])
        self.bf.remove("/A", "PIT1")
        self.assertEqual(self.bf.query("/A"), False)

    def test_fp(self):
        """
        Saturate the Bloom filter,
        and lookup a diffent key expecting a false positive
        """
        for i in range(1024):
            self.bf.add(str(i), "PIT1")
        self.assertEqual(self.bf.query("x"), "FP")

if __name__ == '__main__':
    ut.main(verbosity=2)
