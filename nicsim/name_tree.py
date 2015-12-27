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
    def __init__(self, name, tree, parent, **params):
        self.name = name
        self.tree = tree
        assert isinstance(parent, NameTreeNode) or (parent is None and name == "/")
        self.parent = parent
        self.children = {}
        self._init(**params)

    def _init(self):
        """
        When overridden in a subclass, perform initialization.
        """
        pass

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
        lastComp = "/" if self.name == "/" else nameutil.getLastComponent(self.name)
        return "\n".join([ "%s%s %s" % ("  " * indent, lastComp, self._printAttributes()) ] +
                         [ child.printSubtree(indent + 1) for child in self.iterChildren() ])

    def iterChildren(self):
        """
        Iterate over children of this node.

        Children are sorted by name (string sorting, not NDN canonical order).

        To iterate over children unsorted, use .children.itervalues().
        """
        for name in sorted(self.children.keys()):
            yield self.children[name]

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
        """Node constructor."""
        self.root = None
        """Root node."""

    def root(self):
        """
        Get the root node.

        If it does not exist, returns None.
        """
        return self.get("/")

    def __setitem__(self, name, node):
        raise TypeError("setitem is disallowed")

    def __missing__(self, name):
        if name == "/":
            parent = None
        else:
            parent = self.get(nameutil.getPrefix1(name))
            if parent is None:
                raise KeyError("parent of %s is missing" % name)
        node = self.node(name, tree=self, parent=parent)
        dict.__setitem__(self, name, node)
        if name == "/":
            self.root = node
        else:
            parent.children[name] = node
        return node

    def __delitem__(self, name):
        if name not in self:
            raise KeyError("node does not exist")

        node = self[name]
        if len(node.children) > 0:
            raise KeyError("cannot delete node %s with %d children" % (name, len(node.children)))

        if name == "/":
            self.root = None
        else:
            del node.parent.children[name]
        dict.__delitem__(self, name)

    def _printAttributes(self):
        """
        When overridden in a subclass, print the title and attributes of the tree.

        :rtype str
        """
        return self.__class__.__name__

    def __repr__(self):
        return "%s{%s}" % (self._printAttributes(), ",".join([ str(self[name]) for name in sorted(self.keys()) ]))

    def __str__(self):
        return "%s\n%s" % (self._printAttributes(), "  (empty)" if self.root is None else self.root.printSubtree(indent=1))
