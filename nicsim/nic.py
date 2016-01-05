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
    def __makeBloomFilter(bf, canDisable=False):
        if isinstance(bf, NicBloomFilter):
            return bf
        elif isinstance(bf, (int, long)):
            if bf == 0:
                if canDisable:
                    return None
                else:
                    raise ValueError("Bloom filter size cannot be zero")
            return NicBloomFilter(bf)
        else:
            if bf is None and canDisable:
                return None
            raise TypeError("unexpected type for Bloom filter")

    def __init__(self, bf1, bf2, bf3, ignoreNetType2=False):
        """
        Constructor;

        :param bf1: NicBloomFilter instance or BF size
        :param bf2: NicBloomFilter instance or BF size
        :param bf3: NicBloomFilter instance or BF size; None or 0 to disable BF3
        :param ignoreNetType2: if true, packets are matched against BF2 even if it's not Interest
        """
        self.bf1 = Nic.__makeBloomFilter(bf1)
        self.bf2 = Nic.__makeBloomFilter(bf2)
        self.bf3 = Nic.__makeBloomFilter(bf3, canDisable=True)
        self.ignoreNetType2 = ignoreNetType2

        self._prefixMatch = {
          "I": (self.bf1, "FP1"),
          "D": (self.bf1, "FP1") if self.bf3 is None else (self.bf3, "FP3")
        }

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

        # BF1 or BF3 prefix match
        prefixMatchBf, prefixMatchFpCode = self._prefixMatch[netType]
        for prefix in prefixes:
            result1 = prefixMatchBf.query(prefix)
            if result1 == False:
                pass
            elif result1 == "FP":
                reasonCodes += [prefixMatchFpCode]
            else:
                reasonCodes += result1

        # BF2 exact match for Interest
        if netType == "I" or self.ignoreNetType2:
            result2 = self.bf2.query(name)
            if result2 == False:
                pass
            elif result2 == "FP":
                reasonCodes += ["FP2"]
            else:
                reasonCodes += result2

        return len(reasonCodes) > 0, list(set(reasonCodes))
