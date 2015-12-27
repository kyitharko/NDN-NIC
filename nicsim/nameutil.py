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

def getPrefixes(name):
    """
    Get all prefixes of a name, including itself.
    """
    prefixes = ["/"]
    if name == "/":
        return prefixes

    pos = name.find("/", 1)
    while pos >= 0:
        prefixes.append(name[0:pos])
        pos = name.find("/", pos + 1)

    prefixes.append(name)
    return prefixes

def getPrefix1(name):
    """
    Get one-shorter prefix of a name.
    """
    if name == "/":
        return None
    pos = name.rfind("/")
    assert pos >= 0
    if pos == 0:
        return "/"
    return name[0:pos]

def getLastComponent(name):
    """
    Get last component of a name.
    """
    if name == "/":
        return None
    return name[name.rfind("/")+1:]

if __name__ == "__main__":
    for name in ["/", "/example", "/example/hello/world"]:
        print "name=%s" % name
        print "getPrefixes(name)=%s" % getPrefixes(name)
        print "getPrefix1(name)=%s" % getPrefix1(name)
        print "getLastComponent(name)=%s" % getLastComponent(name)
        print
