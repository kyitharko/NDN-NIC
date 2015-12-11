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
This module defines simulation of NDN-NIC, which contains a NIC simulator and
three tables (PIT, FIB, and CS)
"""

from nic import Nic
from tables import Pit, Fib, Cs

class NicSim:
    """
    Create a new NIC simulator which contains both a nic and three tables

    :param int mBuckets: the size of buckets
    """
    def __init__(self, mBuckets):
        self.nic = Nic(mBuckets)
        self.pit = Pit(self.nic)
        self.fib = Fib(self.nic)
        self.cs = Cs(self.nic)

    def parseTrafficTableTrace(self, inputLine):
        inputList = inputLine.split("\t")
        print "inputList : ", inputList
        traceType = inputList[1]

        outputList = []

        if traceType == "PKT":
            #processing pakcet trace
            packetType = inputList[2]
            packetName = inputList[3]
            accepted, reasonCode = self.nic.processPacket(packetType, packetName)

            print accepted, reasonCode
            #strip \n from last component
            if "\n" in inputList[4]:
                inputList[4] = inputList[4][:-1]

            outputList.append(inputList[0])
            outputList.append(inputList[2])
            outputList.append(inputList[3])
            outputList.append(inputList[4])

            if accepted:
                outputList.append(",".join(reasonCode))
            else:
                outputList.append("DROP")

            print "outputList ",outputList
            return outputList

        elif traceType == "INS":
            tableName = inputList[2]
            packetName = inputList[3]
            if "\n" in packetName:
                packetName = packetName[:-1]

            if tableName == "PIT":
                self.pit.insert(packetName)
            elif tableName == "FIB":
                self.fib.insert(packetName)
            elif tableName == "CS":
                self.cs.insert(packetName)

            print "   BF1", self.nic.bf1
            print "\n   BF2", self.nic.bf2

        elif traceType == "DEL":
            tableName = inputList[2]
            packetName = inputList[3]
            if "\n" in packetName:
                packetName = packetName[:-1]

            if tableName == "PIT":
                self.pit.erase(packetName)
            elif tableName == "FIB":
                self.fib.erase(packetName)
            elif tableName == "CS":
                self.cs.erase(packetName)

            print "   BF1", self.nic.bf1
            print "\n   BF2", self.nic.bf2
