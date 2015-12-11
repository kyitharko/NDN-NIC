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


"""
Main executable for NicSim.
"""

from nic_sim import NicSim
import sys

if __name__ == "__main__":
    nicSim = NicSim(mBuckets=100)

    for line in sys.stdin:
        outputList = nicSim.parseTrafficTableTrace(line)
        if type(outputList) == list:
            print '\t'.join(outputList)
