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
from name_tree import NameTree
from nic import Nic
from nic_sim import NicSim
from table import NopTable, TreeCs, TreeCsNode

class MaxDegreeCsNode(TreeCsNode):
    def addChild(self, child):
        TreeCsNode.addChild(self, child)
        self.tree.maxDegrees[self.name] = max(self.tree.maxDegrees.get(self.name, 0), len(self.children))

class MaxDegreeCsTree(NameTree):
    def __init__(self, **params):
        NameTree.__init__(self, **params)
        self.maxDegrees = {} # name=>maxDegree

class MaxDegreeCs(TreeCs):
    def __init__(self):
        TreeCs.__init__(self, tree=MaxDegreeCsTree, node=MaxDegreeCsNode)

class MaxDegreeCollector(NicSim):
    """
    Estimate packet processing overhead based on packet arrival records.
    """
    def __init__(self):
        NicSim.__init__(self, Nic(1, 1, 1), NopTable(), NopTable(), MaxDegreeCs())

    def processPacketArrival(self, *opts):
        return "X"

    def report(self, os):
        for name, maxDegree in self.cs.tree.maxDegrees.iteritems():
            print >>os, '%s\t%d\t%d' % (name, nameutil.countComponents(name), maxDegree)

if __name__ == "__main__":
    collector = MaxDegreeCollector()
    collector.processTtt(sys.stdin, open(os.devnull, 'w'), open(os.devnull, 'w'))
    collector.report(sys.stdout)
