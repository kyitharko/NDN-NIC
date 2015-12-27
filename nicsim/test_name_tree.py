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

import unittest as ut
from name_tree import NameTree

class NameTreeTestCase(ut.TestCase):
    def test_insert(self):
        nt = NameTree()
        self.assertEqual(nt.root, nt["/"])

        with self.assertRaises(KeyError):
            nt["/A/B"] # parent missing

        nt["/A"]
        nt["/A/B"]
        nt["/A/C"]

        self.assertEqual(len(nt), 4)
        self.assertEqual(nt.root.name, "/")
        self.assertEqual(nt["/A"].name, "/A")

        self.assertEqual(nt["/A"].parent, nt.root)
        self.assertEqual(nt.root.children, {"/A":nt["/A"]})
        self.assertEqual(nt["/A/B"].parent, nt["/A"])
        self.assertEqual(nt["/A"].children, {"/A/B":nt["/A/B"], "/A/C":nt["/A/C"]})

    def test_delete(self):
        nt = NameTree()

        with self.assertRaises(KeyError):
            del nt["/"] # cannot delete root

        nt["/A"]
        nt["/A/B"]
        nt["/A/C"]
        nt["/D"]
        nt["/D/E"]
        nt["/D/F"]
        self.assertEqual(len(nt), 7)

        with self.assertRaises(KeyError):
            del nt["/G"] # node missing

        with self.assertRaises(KeyError):
            del nt["/D"] # cannot delete node with children

        self.assertIn("/D/E", nt)
        del nt["/D/E"]
        self.assertNotIn("/D/E", nt)
        self.assertIn("/D", nt)
        self.assertEqual(len(nt), 6)
        self.assertEqual(nt["/D"].children, {"/D/F":nt["/D/F"]})

        self.assertIn("/D/F", nt)
        del nt["/D/F"]
        self.assertNotIn("/D/F", nt)
        self.assertIn("/D", nt)
        self.assertEqual(nt["/D"].children, {})

        del nt["/D"]
        self.assertNotIn("/D", nt)

if __name__ == '__main__':
    ut.main(verbosity=2)
