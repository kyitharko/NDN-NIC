# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014-2015 Regents of the University of California.
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
	"""
	Test for NicBloomFilter
	"""

	def setup(self):
		self.NBF = NicBloomFilter(100)

	def test_add_query_true(self):
		"""
		Add ("/ndn/test","PIT) into NicBloomFilter
		and make a query of "/ndn/test"
		"""

		NBF = NicBloomFilter(100)
		NBF.add("/ndn/test","PIT")
		result = NBF.query("/ndn/test")
		self.assertTrue(result, "Query result is invalid")

	def test_add_query_false(self):
		"""
		Add ("/ndn/test","PIT) into NicBloomFilter
		and make a query of "/ndn/test1"
		"""

		NBF = NicBloomFilter(100)
		NBF.add("/ndn/test","PIT")
		result = NBF.query("/ndn/test1")
		self.assertFalse(result, "Query result is invalid")

	def test_add_query_FP(self):
		"""
		Add multiple keys into NicBloomFilter to achieve FP
		and make a query of diffent key with FP
		"""

		NBF = NicBloomFilter(100)
		for i in range(200):
			NBF.add(str(i),"PIT")
		result = NBF.query("300")
		self.assertEqual(result,"FP", "Query result is invalid")


if __name__ == '__main__':
    ut.main(verbosity=2)