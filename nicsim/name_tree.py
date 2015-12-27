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

class NameTreeNode:
    """
    Represents a node in NameTree.
    """
    def __init__(self, name, parent):
        self.name = name
        assert isinstance(parent, NameTreeNode) or (parent is None and name == "/")
        self.parent = parent
        self.children = {}

    def _printAttributes(self):
        """
        When overridden in a subclass, print the attributes of this node.

        :rtype str
        """
        return ""

    def __repr__(self):
        return "<%s %s>" % (self.name, self._printAttributes())

    def printSubtree(self, indent=0):
        """
        Print the subtree rooted at this node.

        :param int indent: indentation level
        :
        """
        lastComp = nameutil.getLastComponent(self.name)
        return "\n".join([ "%s%s %s" % ("  " * indent, lastComp, self._printAttributes()) ] +
                         [ self.children[child].printSubtree(indent + 1) for child in sorted(self.children.keys()) ])

class NameTree(dict):
    """
    Represents a tree of name hierarchy.
    """
    def __init__(self, node=NameTreeNode):
        """
        Construct a NameTree.

        :param class node: node constructor
        """
        self.node = node
        dict.__setitem__(self, "/", self.node("/", parent=None))
        self.root = self["/"]
        """The root node. This node cannot be deleted."""

    def __setitem__(self, name, node):
        raise TypeError("setitem is disallowed")

    def __missing__(self, name):
        parent = self.get(nameutil.getPrefix1(name))
        if parent is None:
            raise KeyError("parent node of %s does not exist" % name)
        node = self.node(name, parent=parent)
        dict.__setitem__(self, name, node)
        parent.children[name] = node
        return node

    def __delitem__(self, name):
        if name not in self:
            raise KeyError("node does not exist")
        if name == "/":
            raise KeyError("cannot delete root node")

        node = self[name]
        if len(node.children) > 0:
            raise KeyError("cannot delete node %s with %d children" % (name, len(node.children)))

        del node.parent.children[name]
        dict.__delitem__(self, name)

    def __repr__(self):
        return "%s{%s}" % (self.name, ",".join([ str(self[name]) for name in sorted(self.keys()) ]))

    def __str__(self):
        return "%s\n%s" % (self.name, self.root.printSubtree(indent=1))
