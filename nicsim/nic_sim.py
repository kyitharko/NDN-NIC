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

from nic import Nic
from table import NaiveFib, NaivePit, NaiveCs

class NicSim:
    """
    The NDN-NIC simulator.
    This class simulates a hardware NDN-NIC and its corresponding software portion.
    """
    def __init__(self, nic, fib=NaiveFib, pit=NaivePit, cs=NaiveCs):
        """
        Constructor.

        :param Nic nic: an NDN-NIC hardware simulator
        :param fib: FIB constructor or instance
        :param pit: PIT constructor or instance
        :param cs: CS constructor or instance
        """
        if not isinstance(nic, Nic):
            raise TypeError("unexpected type for Nic")
        self.nic = nic

        def makeTable(tableName, table):
            import inspect
            if inspect.isclass(table):
                return table(nic)
            elif hasattr(table, "insert") and hasattr(table, "erase") and \
                 table.insert.im_self is not None:
                return table
            else:
                raise TypeError("unexpected type for %s" % tableName)

        self.fib = makeTable("FIB", fib)
        self.pit = makeTable("PIT", pit)
        self.cs = makeTable("CS", cs)

    def processPacketArrival(self, timestamp, _pkt, netType, name, pktSize, swDecision):
        """
        Process a packet arrival line from Traffic and Table Trace.
        """
        accepted, reasonCodes = self.nic.processPacket(netType, name)

        if accepted:
            return ",".join(reasonCodes)
        else:
            return "DROP"

    def processTableChange(self, timestamp, act, table, name):
        """
        Process a table change line from Traffic and Table Trace.
        """
        self.nic.bf1.beginUpdate()
        self.nic.bf2.beginUpdate()
        if self.nic.bf3 is not None:
            self.nic.bf3.beginUpdate()

        tbl = getattr(self, table.lower())
        func = {"INS": "insert", "DEL": "erase"}[act]
        getattr(tbl, func)(name)

        (bf1sets, bf1clears) = self.nic.bf1.endUpdate()
        (bf2sets, bf2clears) = self.nic.bf2.endUpdate()
        (bf3sets, bf3clears) = self.nic.bf3.endUpdate() if self.nic.bf3 is not None else (0, 0)
        return bf1sets, bf1clears, bf2sets, bf2clears, bf3sets, bf3clears

    def processTtt(self, tttFile, ndFile, bfuFile):
        """
        Process a Traffic and Table Trace file.
        """
        for line in tttFile:
            columns = line.rstrip().split("\t")
            if len(columns) == 6 and columns[1] == "PKT":
                decision = self.processPacketArrival(*columns)
                del columns[4]
                del columns[1]
                columns.append(decision)
                print >>ndFile, "\t".join(columns)
            elif len(columns) == 4:
                bfuCounts = self.processTableChange(*columns)
                columns += [ str(c) for c in bfuCounts ]
                print >>bfuFile, "\t".join(columns)

if __name__ == "__main__":
    nic = Nic(128, 128, 128)
    nicSim = NicSim(nic)

    import sys
    nicSim.processTtt(sys.stdin, sys.stdout, sys.stdout)
