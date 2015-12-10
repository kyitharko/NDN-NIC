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
This module defines XOR hash function

ref paper: DEEP PACKET INSPECTION USING PARALLEL BLOOM FILTERS
"""
import random

class XorHashes:
	"""
	Create a new XorHashes with multiple XOR hashes and a collection compute
	functions

	:param int nHashes: the number of hashes the XorHashes contains
	:param int m: the bound size m
	"""
	def __init__(self, nHashes, m):
		#randomNumbers: nHashes sets of pre-determined random numbers for XorHashes
		#suppose each set has 500*8 number of values
		self.randomNumbers = {}
		self.nHashes = nHashes
		randomNumberSize = 500*8

		for i in range(nHashes):
			self.randomNumbers[i] = []
			for j in range(randomNumberSize):
				self.randomNumbers[i].append(random.randint(0, m-1))

	def XOR(self, randomNumbers, name):
		"""
		compute XOR hash value with input random numbers

		:param list randomNumbers: a list of random numbers
		:param string name: the name waiting to bu hashed
		:return: h
		:rtype: int
		"""
		randomIndex = 0
		h = 0

		for c in name:
			for i in range(8):
				h ^= (1<<i)&ord(c)*randomNumbers[randomIndex]
				randomIndex += 1

		h ^= 0

		return h


	def computeHashes(self, name):
		"""
		compute nHashes XOR hash values 

		:param string name: the name waiting to bu hashed
		:return: hashes
		:rtype: list
		"""
		hashes = []
		for i in range(self.nHashes):
			hashes.append( self.XOR(self.randomNumbers[i], name) )

		return hashes


