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

from nic_bloom_filter import NicBloomFilter
from utility import getPrefixes

class Nic:
    """
    Simulates NDN-NIC hardware.
    """

    def __init__(self, mBuckets):
        self.bf1 = NicBloomFilter(mBuckets)
        self.bf2 = NicBloomFilter(mBuckets)

    def processPacket(self, netType, name):
        """
        Process packet log line

        :param string netType: network layer type of the packet; possible values are:
                                * **I**: Interest
                                * **D**: Data
        :param string name: Interest or Data Name
        :return: accepted, reasonCode
        :rtype: bool, string
        """
        accepted = False
        reasonCodes = []

        # get prefixes of the input name
        prefixes = getPrefixes(name)

        # BF1 prefix match
        for prefix in prefixes:
            result1 = self.bf1.query(prefix)
            if result1 == False:
                pass
            elif result1 == "FP":
                accepted = True
                reasonCodes += ["FP1"]
            else:
                accepted = True
                reasonCodes += result1

        # BF2 exact match
        result2 = self.bf2.query(name)
        if result2 == False:
            pass
        elif result2 == "FP":
            accepted = True
            reasonCodes += ["FP2"]
        else:
            accepted = True
            reasonCodes += result2

        return accepted, reasonCodes
