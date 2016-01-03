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

import nameutil
from name_tree import NameTree, NameTreeNode

class AitNode(NameTreeNode):
    """
    AIT node.
    """
    def _init(self):
        self.inCs = False
        """whether this name has a CS entry"""
        self.hasCs1 = False
        """whether this name has a CS1 key"""
        self.hasCs2 = False
        """whether this name has a CS2 key"""
        self.hasFib1 = False
        """whether this name has a FIB1 key"""

        self.deepestCs2Dist = None
        """distance to deepest CS2 key"""
        self.deepestCs2Ptr = None
        """reference of the subtree containing deepest CS2 key"""

        self.nCs1Descendants = 0
        """count of descendants with CS1 key"""
        self.deepestMultiCs1Dist = None
        """distance to deepest CS2 key with two or more CS1 descendants"""
        self.deepestMultiCs1Ptr = None
        """reference of the subtree containing deepest CS2 key with two or more CS1 descendants"""

    def _printAttributes(self):
        return "".join([
                         "inCs " if self.inCs else "",
                         "CS1 " if self.hasCs1 else "",
                         "CS2 " if self.hasCs2 else "",
                         "FIB1 " if self.hasFib1 else "",
                       ] +
                       ([
                         "deep2=none " if self.deepestCs2Dist is None
                         else "deep2=self " if self.deepestCs2Dist == 0
                         else "deep2=(%d,%s) " % (self.deepestCs2Dist, nameutil.getLastComponent(self.deepestCs2Ptr.name)),
                         "nCS1=%d " % self.nCs1Descendants,
                         "deep1=none " if self.deepestMultiCs1Dist is None
                         else "deep1=self " if self.deepestMultiCs1Dist == 0
                         else "deep1=(%d,%s) " % (self.deepestMultiCs1Dist, nameutil.getLastComponent(self.deepestMultiCs1Ptr.name)),
                       ] if self.hasCs2 else [])
                      )

    def labelCs2(self):
        """
        Add CS2 key for this node.
        """
        if self.hasCs2:
            return
        self.unlabelCs1()
        self.hasCs2 = True
        self.tree.bf2.add(self.name, "CS2")
        self.tree.nCs2 += 1

        self._updateCs2Fields()

    def unlabelCs2(self):
        """
        Remove CS2 key for this node.
        """
        if not self.hasCs2:
            return
        for child in self.children.itervalues():
            child.unlabelCs1()
            child.unlabelCs2()
        self.hasCs2 = False
        self.tree.bf2.remove(self.name, "CS2")
        self.tree.nCs2 -= 1

        self.deepestCs2Dist = None
        self.deepestCs2Ptr = None
        self.nCs1Descendants = 0
        self.deepestMultiCs1Dist = None
        self.deepestMultiCs1Ptr = None

        if self.parent is not None:
            self.parent._updateCs2Fields()

    def labelCs1(self):
        """
        Add CS1 key for this node, and remove CS2 keys for descendants.
        """
        if self.hasCs1:
            return
        self.unlabelCs2()
        self.hasCs1 = True
        self.tree.bf1.add(self.name, "CS1")
        self.tree.nCs1 += 1

        if self.parent is not None:
            self.parent._updateCs2Fields()

    def unlabelCs1(self):
        """
        Remove CS1 key for this node.
        """
        if not self.hasCs1:
            return
        self.hasCs1 = False
        self.tree.bf1.remove(self.name, "CS1")
        self.tree.nCs1 -= 1

        if self.parent is not None:
            self.parent._updateCs2Fields()

    def _updateCs2Fields(self):
        assert self.hasCs2

        self.deepestCs2Dist = 0
        self.deepestCs2Ptr = None
        self.nCs1Descendants = 0
        self.deepestMultiCs1Dist = None
        self.deepestMultiCs1Ptr = None

        for child in self.iterChildren():
            if child.hasCs1:
                self.nCs1Descendants += 1
            if not child.hasCs2:
                continue
            if child.deepestCs2Dist + 1 > self.deepestCs2Dist:
                self.deepestCs2Dist = child.deepestCs2Dist + 1
                self.deepestCs2Ptr = child
            self.nCs1Descendants += child.nCs1Descendants
            if child.deepestMultiCs1Dist is not None and \
               (self.deepestMultiCs1Dist is None or child.deepestMultiCs1Dist + 1 > self.deepestMultiCs1Dist):
                self.deepestMultiCs1Dist = child.deepestMultiCs1Dist + 1
                self.deepestMultiCs1Ptr = child

        if self.nCs1Descendants >= 2 and self.deepestMultiCs1Dist is None:
            self.deepestMultiCs1Dist = 0

        if self.parent is not None:
            self.parent._updateCs2Fields()

    def findReduction2(self):
        """
        Find a target for FP2 reduction within this subtree.
        """
        if self.deepestCs2Dist is None:
            return None
        if self.deepestCs2Dist == 0:
            return self
        return self.deepestCs2Ptr.findReduction2()

    def findReduction1(self):
        """
        Find a target for FP1 reduction within this subtree.
        """
        if self.deepestMultiCs1Dist is None:
            return None
        if self.deepestMultiCs1Dist == 0:
            return self
        return self.deepestMultiCs1Ptr.findReduction1()

class Ait(NameTree):
    """
    Acceptable Interest Tree.
    """
    def __init__(self, bf1, bf2):
        NameTree.__init__(self, node=AitNode)
        self.bf1 = bf1
        self.bf2 = bf2
        self.nCs1 = 0
        self.nCs2 = 0

    def _printAttributes(self):
        return "AIT nCS1=%d nCS2=%d" % (self.nCs1, self.nCs2)

    def checkInvariants(self):
        """
        Check invariants of AIT.

        * All nodes are covered by either CS1 key or CS2 key.
        * A node is not both CS1 and CS2.
        * CS1 key has no labelled descendants.
        """
        def checkSubtree(node, isCoveredByCs1):
            if isCoveredByCs1:
                assert not node.hasCs1
                assert not node.hasCs2
            elif node.hasCs2:
                assert not node.hasCs1
            elif node.hasCs1:
                assert not node.hasCs2
                isCoveredByCs1 = True
            for child in node.children.itervalues():
                checkSubtree(child, isCoveredByCs1)

        if self.root is not None:
            checkSubtree(self.root, False)

class AitCsOptions:
    useFreeFib1 = False
    """Use "free" CS1 key where FIB1 key exists."""
    degreeThreshold = 64
    """Node degree threshold. A node exceeding this threshold is labelled CS1."""
    fp2Threshold = 0.1
    """BF2 false positive threshold."""
    bf2Capacity = None
    """BF2 capacity, specified as number of keys."""
    fp1Threshold = 0.1
    """BF1 false positive threshold."""
    bf1Capacity = None
    """BF1 capacity, specified as number of keys."""

    def __init__(self, **params):
        for k, v in params.iteritems():
            if not hasattr(self, k):
                raise KeyError("unknown attribute %s" % k)
            setattr(self, k, v)

class AitCs:
    """
    ContentStore based on AIT.
    """
    def __init__(self, nic, options=AitCsOptions()):
        self.options = options
        self.bf1 = nic.bf1
        self.bf2 = nic.bf2
        self.ait = Ait(self.bf1, self.bf2)

    def insert(self, name):
        # update AIT
        newNodes = []
        for prefix in nameutil.getPrefixes(name):
            isNewNode = prefix not in self.ait
            node = self.ait[prefix]
            if isNewNode:
                node.hasFib1 = "FIB1" in self.bf1.table.get(name, [])
                newNodes.append(node)
        node.inCs = True # node refers to the ait[name]
        if len(newNodes) == 0:
            return

        # do nothing if already covered
        parentNode = newNodes[0].parent
        if parentNode is not None and not parentNode.hasCs2:
            # It's sufficient to check the parent of the top new node,
            # because that node must be covered previously.
            # If the parent has CS2, it means there's no CS1 in ancestors,
            # and therefore the new nodes are not covered.
            # Otherwise, the parent is covered by a CS1 key either on itself or an ancestor,
            # which implies new nodes are also covered by that CS1 key.
            return

        # use "free" CS1 key
        if self.options.useFreeFib1:
            raise NotImplementedError

        # add CS2 keys
        for node in newNodes:
            node.labelCs2()

        # check degree threshold
        if parentNode is not None and len(parentNode.children) > self.options.degreeThreshold:
            assert parentNode.hasCs2
            parentNode.labelCs1()

        # FP2 reduction
        bf2Capacity = self.bf2.capacity(self.options.fp2Threshold) if self.options.bf2Capacity is None \
                      else self.options.bf2Capacity
        while len(self.bf2) > bf2Capacity:
            target = self.ait.root.findReduction2()
            if target is None:
                break
            target.labelCs1()

        # FP1 reduction
        bf1Capacity = self.bf1.capacity(self.options.fp1Threshold) if self.options.bf1Capacity is None \
                      else self.options.bf1Capacity
        while len(self.bf1) > bf1Capacity:
            target = self.ait.root.findReduction1()
            if target is None:
                break
            target.labelCs1()

        self.ait.checkInvariants()

    def erase(self, name):
        raise NotImplementedError

AitCs.Options = AitCsOptions

if __name__ == "__main__":
    from nic import Nic
    nic = Nic(128, 128)
    options = AitCsOptions(useFreeFib1=False, bf2Capacity=8, bf1Capacity=8)
    cs = AitCs(nic, options)
    print cs.ait
    names = [ "/".join(["", c1, c2, c3]) for c1 in "ABCD" for c2 in "abcd" for c3 in "1234" ]
    for name in names:
        cs.insert(name)
        print cs.ait
