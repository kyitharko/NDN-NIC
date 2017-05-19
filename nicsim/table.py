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
