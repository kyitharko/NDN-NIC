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

import nameutil

from ait import ActiveCs
from name_tree import NameTree, NameTreeNode

class NopTable:
    def insert(self, name):
        pass

    def erase(self, name):
        pass

class DirectFib:
    """
    A FIB that adds every entry name to BF-FIB.
    """
    def __init__(self, nic):
        self.bfFib = nic.bfFib

    def insert(self, name):
        self.bfFib.add(name, "FIB")

    def erase(self, name):
        self.bfFib.remove(name, "FIB")

class DirectPit:
    """
    A PIT that adds every entry name to BF-PIT.
    """
    def __init__(self, nic):
        self.bfPit = nic.bfPit

    def insert(self, name):
        self.bfPit.add(name, "PIT")

    def erase(self, name):
        self.bfPit.remove(name, "PIT")

class DirectCs:
    """
    A CS that adds prefixes of every entry name to BF-CS.
    """
    def __init__(self, nic):
        self.bfCs = nic.bfCs

    def insert(self, name):
        for prefix in nameutil.getPrefixes(name):
            self.bfCs.add(prefix, "CS2")

    def erase(self, name):
        for prefix in nameutil.getPrefixes(name):
            self.bfCs.remove(prefix, "CS2")

class BasicCs:
    """
    A CS that adds prefixes of every entry name to BF-CS except those covered by a FIB entry.

    .. warning:: This implementation does not accommodate FIB entry removal.
    """
    def __init__(self, nic):
        self.bfFib = nic.bfFib
        self.bfCs = nic.bfCs

    def insert(self, name):
        for prefix in nameutil.getPrefixes(name):
            if "FIB" in self.bfFib.table.get(prefix, []):
                self.bfFib.add(prefix, "CS1")
                break
            else:
                self.bfCs.add(prefix, "CS2")

    def erase(self, name):
        for prefix in nameutil.getPrefixes(name):
            if "CS1" in self.bfFib.table.get(prefix, []):
                self.bfFib.remove(prefix, "CS1")
                break
            else:
                self.bfCs.remove(prefix, "CS2")

class TreeCsNode(NameTreeNode):
    def _init(self):
        self.inCs = False

    def _printAttributes(self):
        return "CS " if self.inCs else ""

    def lookup(self):
        if self.inCs:
            return self.name, 0
        cost = 0
        for child in self.iterChildren():
            found, c = child.lookup()
            cost += 1 + c
            if found is not None:
                return found, cost
        return None, cost

class TreeCs:
    def __init__(self, tree=NameTree, node=TreeCsNode):
        assert issubclass(node, TreeCsNode)
        assert issubclass(tree, NameTree)
        self.tree = tree(node=node)

    def insert(self, name):
        for prefix in nameutil.getPrefixes(name):
            node = self.tree[prefix]

        node.inCs = True # node refers to the tree[name]

    def erase(self, name):
        node = self.tree[name]
        node.inCs = False

        while node is not None and node.inCs is False and len(node.children) == 0:
            parent = node.parent
            del self.tree[node.name]
            node = parent

    def computeLookupCost(self, name):
        if name not in self.tree:
            return 0
        found, cost = self.tree[name].lookup()
        return cost
