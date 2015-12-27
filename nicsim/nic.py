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
import nameutil

class Nic:
    """
    Simulates NDN-NIC hardware.
    """
    @staticmethod
    def __makeBloomFilter(bf):
        if isinstance(bf, NicBloomFilter):
            return bf
        elif isinstance(bf, (int, long)):
            return NicBloomFilter(bf)
        else:
            raise TypeError("unexpected type for Bloom filter")

    def __init__(self, bf1, bf2):
        self.bf1 = Nic.__makeBloomFilter(bf1)
        self.bf2 = Nic.__makeBloomFilter(bf2)

    def processPacket(self, netType, name):
        """
        Determine whether to accept or drop a packet.

        :param string netType: network layer type of the packet, either I or D
        :param string name: Interest or Data Name
        :return: accepted, reasonCodes
        :rtype: bool, list of strings
        """
        reasonCodes = []

        # get prefixes of the input name
        prefixes = nameutil.getPrefixes(name)

        # BF1 prefix match
        for prefix in prefixes:
            result1 = self.bf1.query(prefix)
            if result1 == False:
                pass
            elif result1 == "FP":
                reasonCodes += ["FP1"]
            else:
                reasonCodes += result1

        # BF2 exact match
        result2 = self.bf2.query(name)
        if result2 == False:
            pass
        elif result2 == "FP":
            reasonCodes += ["FP2"]
        else:
            reasonCodes += result2

        return len(reasonCodes) > 0, reasonCodes
