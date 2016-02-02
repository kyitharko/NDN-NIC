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

from ait import AitCs

class NaiveFib:
    """
    A FIB that adds every entry name to BF1.
    """
    def __init__(self, nic):
        self.bf1 = nic.bf1

    def insert(self, name):
        self.bf1.add(name, "FIB1")

    def erase(self, name):
        self.bf1.remove(name, "FIB1")

class NaivePit:
    """
    A PIT that adds every entry name to BF3.
    """
    def __init__(self, nic):
        self.bf, self.reasonCode = (nic.bf1, "PIT1") if nic.bf3 is None else (nic.bf3, "PIT3")

    def insert(self, name):
        self.bf.add(name, self.reasonCode)

    def erase(self, name):
        self.bf.remove(name, self.reasonCode)

class NaiveCs:
    """
    A CS that adds prefixes of every entry name to BF2.
    """
    def __init__(self, nic):
        self.bf2 = nic.bf2

    def insert(self, name):
        prefixes = nameutil.getPrefixes(name)
        for prefix in prefixes:
            self.bf2.add(prefix, "CS2")

    def erase(self, name):
        prefixes = nameutil.getPrefixes(name)
        for prefix in prefixes:
            self.bf2.remove(prefix, "CS2")

class BasicCs:
    """
    A CS that adds prefixes of every entry name to BF2 except those covered by a FIB1 key.
    """
    def __init__(self, nic):
        self.bf1 = nic.bf1
        self.bf2 = nic.bf2

    def insert(self, name):
        prefixes = nameutil.getPrefixes(name)
        for prefix in prefixes:
            if "FIB1" in self.bf1.table.get(prefix, []):
                self.bf1.add(prefix, "CS1")
                break
            else:
                self.bf2.add(prefix, "CS2")

    def erase(self, name):
        prefixes = nameutil.getPrefixes(name)
        for prefix in prefixes:
            if "CS1" in self.bf1.table.get(prefix, []):
                self.bf1.remove(prefix, "CS1")
                break
            else:
                self.bf2.remove(prefix, "CS2")
