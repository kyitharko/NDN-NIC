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


"""
This module defines simulation of NIC with two bloom filters
"""

from nic_bloom_filter import NicBloomFilter

class Nic:
    """
    Create a new NIC which contains two nic bloom filters
    """

    def __init__(self, mBuckets):
        self.bf1 = NicBloomFilter(m)
        self.bf2 = NicBloomFilter(m)

    def processPacket(self, netType, name):
        """
        Process packet log line

        :param string netType: network layer type of the packet; possible values are:
                                * **I**: Interest
                                * **D**: Data
        :param string name: Uri format of name with "/"
        :return: accepted, reasonCode
        :rtype: bool, string
        """
        accepted = False
        reasonCode = []


        
        #Get prefixes of the input name
        prefixes = ['/'] 
        components = name.split('/')
     
        for i in range(2,components+1):
            prefix = '/'.join(components[:i])
            prefixes.append(prefix)

        print prefixes

        #check each prefix in bf1 - PIT, FIB, part CS
        for prefix in prefixes:
            result = self.bf1.query(prefix)
            if result != False:
                accepted = True
                reasonCode += result

        #check the exact name in bf2 - CS
        result = self.bf2.query(name)
        if result != False:
            accepted = True
            reasonCode += result

        return accepted, reasonCode                        



	