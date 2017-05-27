# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2015-2016 Arizona Board of Regents
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

import os
import sys
import nameutil
from nic import Nic
from nic_sim import NicSim
from table import NopTable, TreeCs

class PacketProcessingOverheadEstimator(NicSim):
    """
    Estimate packet processing overhead based on packet arrival records.
    """
    def __init__(self):
        NicSim.__init__(self, Nic(1, 1, 1), NopTable(), NopTable(), TreeCs())

    def processPacketArrival(self, timestamp, _pkt, netType, name, pktSize, swDecision):
        func = {"I": "processInterest", "D": "processData"}[netType]
        return str(getattr(self, func)(name))

    def processInterest(self, name):
        """
        Estimate NameTree node access count for Interest processing.
        1. From root, find or create PIT entry.
        2. From PIT entry node, find matching CS entry, if any.
        """
        return nameutil.countComponents(name) + self.cs.computeLookupCost(name)

    def processData(self, name):
        """
        Estimate NameTree node access count for Data processing.
        1. From root, find matching PIT entries.
        2. Insert CS entry.
        """
        return nameutil.countComponents(name)

if __name__ == "__main__":
    estimator = PacketProcessingOverheadEstimator()
    estimator.processTtt(sys.stdin, sys.stdout, open(os.devnull, 'w'))
