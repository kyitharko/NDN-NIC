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

import sys
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

        self.shallowestCs1Dist = None
        """distance to shallowest CS1 key"""
        self.shallowestCs1Ptr = None
        """reference of the subtree containing shallowest CS1 key"""

    def _printAttributes(self):
        return "".join(
            [
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
              "shallow1=none " if self.shallowestCs1Dist is None
              else "shallow1=(%d,%s) " % (self.shallowestCs1Dist, nameutil.getLastComponent(self.shallowestCs1Ptr.name)),
             ] if self.hasCs2 else [])
            )

    def _trace(self, line):
        self.tree._trace(line)

    def labelCs2(self):
        """
        Add CS2 key for this node.
        """
        if self.hasCs2:
            return 0
        self.unlabelCs1()

        self.hasCs2 = True
        self.tree.bf2.add(self.name, "CS2")
        self.tree.nCs2 += 1
        self._trace("labelCs2 %s" % self.name)

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
        self._trace("unlabelCs2 %s" % self.name)

        self._clearCs2Fields()

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
        self._trace("labelCs1 %s" % self.name)

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
        self._trace("unlabelCs1 %s" % self.name)

        if self.parent is not None:
            self.parent._updateCs2Fields()

    def _clearCs2Fields(self):
        self.deepestCs2Dist = 0
        self.deepestCs2Ptr = None
        self.nCs1Descendants = 0
        self.deepestMultiCs1Dist = None
        self.deepestMultiCs1Ptr = None
        self.shallowestCs1Dist = None
        self.shallowestCs1Ptr = None

    def _updateCs2Fields(self):
        """
        Update shortcut fields on CS2 keys.
        """
        assert self.hasCs2
        self._clearCs2Fields()

        for child in self.iterChildren():
            if child._isPmfpReductionEligible():
                self.nCs1Descendants += 1
                self.shallowestCs1Dist = 1
                self.shallowestCs1Ptr = child
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
            if child.shallowestCs1Dist is not None and \
               (self.shallowestCs1Dist is None or child.shallowestCs1Dist + 1 < self.shallowestCs1Dist):
                self.shallowestCs1Dist = child.shallowestCs1Dist + 1
                self.shallowestCs1Ptr = child

        if self.nCs1Descendants >= 2 and self.deepestMultiCs1Dist is None:
            self.deepestMultiCs1Dist = 0

        self._trace("updateCs2Fields %s nChildren=%d" % (self.name, len(self.children)))

        if self.parent is not None:
            self.parent._updateCs2Fields()

    def _isPmfpReductionEligible(self):
        return self.hasCs1 and len(self.children) <= self.tree.degreeThreshold

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

    def findReductionPmfp(self):
        """
        Find a target for PMFP reduction within this subtree.
        """
        if self._isPmfpReductionEligible():
            return self
        if self.shallowestCs1Dist is None:
            return None
        return self.shallowestCs1Ptr.findReductionPmfp()

DEFAULT_DEGREE_THRESHOLD = 64

class Ait(NameTree):
    """
    Acceptable Interest Tree.
    """
    def __init__(self, bf1, bf2, degreeThreshold=DEFAULT_DEGREE_THRESHOLD, trace=None):
        """
        Constructor.

        :param int degreeThreshold: maximum degree of a node for eligibility in findReductionPmfp
        :param file trace: a file-like object to write trace logs, or None to disable trace logs
        """
        NameTree.__init__(self, node=AitNode)
        self.bf1 = bf1
        self.bf2 = bf2
        self.degreeThreshold = degreeThreshold
        self.trace = trace

        self.nCs1 = 0
        """count of CS1 keys"""
        self.nCs2 = 0
        """count of CS2 keys"""

    def _printAttributes(self):
        return "AIT nCS1=%d nCS2=%d" % (self.nCs1, self.nCs2)

    def _trace(self, line):
        if self.trace is not None:
            self.trace.write(line + "\n")

    def checkInvariants(self):
        """
        Check invariants of AIT.

        * All nodes are covered by either CS1 key or CS2 key.
        * A node is not both CS1 and CS2.
        * CS1 key has no labelled descendants.
        * CS2 node degree is within threshold.
        """
        def checkSubtree(node, isCoveredByCs1):
            if isCoveredByCs1:
                assert not node.hasCs1
                assert not node.hasCs2
            elif node.hasCs2:
                assert not node.hasCs1
                assert len(node.children) <= self.degreeThreshold
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
    degreeThreshold = DEFAULT_DEGREE_THRESHOLD
    """Node degree threshold. A node exceeding this threshold is labelled CS1."""
    fp2Threshold = (None, 0.1, 2)
    """BF2 false positive thresholds.
       Either specify (low, high) limits as a tuple,
       or specify (None, high, multipler) to compute low capacity limit as high - multiplier*degreeThreshold."""
    bf2Capacity = None
    """BF2 capacity, specified as number of keys. This precedes fp2Threshold.
       Either specify (low, high) limits as a tuple,
       or specify (None, high, multipler) to compute low capacity limit as high - multiplier*degreeThreshold."""
    fp1Threshold = (None, 0.1, 2)
    """BF1 false positive threshold.
       Either specify (low, high) limits as a tuple,
       or specify (None, high, multipler) to compute low capacity limit as high - multiplier*degreeThreshold."""
    bf1Capacity = None
    """BF1 capacity, specified as number of keys. This precedes fp1Threshold.
       Either specify (low, high) limits as a tuple,
       or specify (None, high, multipler) to compute low capacity limit as high - multiplier*degreeThreshold."""
    lowLimitMultiplier = 2.0
    """Parameter to compute capacity low limit in case it's unspecified."""

    def __init__(self, **params):
        for k, v in params.iteritems():
            if not hasattr(self, k):
                raise KeyError("unknown attribute %s" % k)
            setattr(self, k, v)

class AitCs:
    """
    ContentStore based on AIT.
    """
    def __init__(self, nic, options=AitCsOptions(), trace=None):
        self.options = options
        self.bf1 = nic.bf1
        self.bf2 = nic.bf2
        self.ait = Ait(self.bf1, self.bf2, degreeThreshold=options.degreeThreshold, trace=trace)

        self.bf2Low, self.bf2High = self._computeLimits(self.bf2, "BF2", self.options.bf2Capacity, self.options.fp2Threshold)
        self.bf1Low, self.bf1High = self._computeLimits(self.bf1, "BF1", self.options.bf1Capacity, self.options.fp1Threshold)
        self._trace("AitCs.bf2Low=%f" % self.bf2Low)
        self._trace("AitCs.bf2High=%f" % self.bf2High)
        self._trace("AitCs.bf1Low=%f" % self.bf1Low)
        self._trace("AitCs.bf1High=%f" % self.bf1High)

    def _computeLimits(self, bf, bfLabel, capacityOption, thresholdOption):
        if capacityOption is None:
            if thresholdOption is None:
                raise ValueError("either capacity or threshold must be specified for %s" % bfLabel)
            return self._computeLimits(bf, bfLabel,
                   [ None if x is None else x if i >= 2 else bf.capacity(x) for i,x in enumerate(thresholdOption) ], None)

        if len(capacityOption) == 2:
            low, high = capacityOption
            if high - low < self.options.degreeThreshold:
                sys.stderr.write("%s capacity limits %f, %f are closer than degreeThreshold\n" % (bfLabel, low, high))
        elif len(capacityOption) == 3:
            low, high, multiplier = capacityOption
            low = high - multiplier * self.options.degreeThreshold
        else:
            raise ValueError("invalid %s threshold or capacity" % bfLabel)

        return low, high

    def _trace(self, line):
        self.ait._trace(line)

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
        self._trace("insert %s nNewNodes=%d" % (name, len(newNodes)))
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
            self._trace("parentDegree %s degree=%d" % (parentNode.name, len(parentNode.children)))
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
            self._trace("exceedDegree %s degree=%d" % (parentNode.name, len(parentNode.children)))
            parentNode.labelCs1()

        # FP2 reduction
        while len(self.bf2) > self.bf2High:
            target = self.ait.root.findReduction2()
            self._trace("reduction2 bf2=%d %s" % (len(self.bf2), "none" if target is None else target.name))
            if target is None:
                break
            target.labelCs1()

        # FP1 reduction
        while len(self.bf1) > self.bf1High:
            target = self.ait.root.findReduction1()
            self._trace("reduction1 bf1=%d %s" % (len(self.bf1), "none" if target is None else target.name))
            if target is None:
                break
            target.labelCs1()

        self.ait.checkInvariants()

    def erase(self, name):
        # update AIT
        assert name in self.ait
        node = self.ait[name]
        assert node.inCs
        node.inCs = False

        erasedNodes = []
        while node is not None:
            if node.inCs or len(node.children) > (0 if len(erasedNodes) == 0 else 1):
                break
            erasedNodes.append(node)
            node = node.parent
        self._trace("erase %s nErasedNodes=%d" % (name, len(erasedNodes)))
        for node in erasedNodes:
            node.unlabelCs2()
            node.unlabelCs1()
            del self.ait[node.name]

        # PMFP reduction
        while len(self.ait) > 0 and len(self.bf2) < self.bf2Low and len(self.bf1) < self.bf1Low:
            target = self.ait.root.findReductionPmfp()
            self._trace("reductionPmfp bf2=%d bf1=%d %s" % (len(self.bf2), len(self.bf1), "none" if target is None else target.name))
            if target is None:
                break
            target.labelCs2()
            for child in target.iterChildren():
                child.labelCs1()

        self.ait.checkInvariants()

AitCs.Options = AitCsOptions

if __name__ == "__main__":
    from nic import Nic
    nic = Nic(128, 128, 0)
    options = AitCsOptions(useFreeFib1=False, bf2Capacity=(5,8), bf1Capacity=(5,8))
    cs = AitCs(nic, options, trace=sys.stderr)
    print cs.ait
    names = [ "/".join(["", c1, c2, c3]) for c1 in "ABCD" for c2 in "abcd" for c3 in "1234" ]
    for name in names:
        print "INS %s" % name
        cs.insert(name)
        print cs.ait
    names.reverse()
    for name in names:
        print "DEL %s" % name
        cs.erase(name)
        print cs.ait
