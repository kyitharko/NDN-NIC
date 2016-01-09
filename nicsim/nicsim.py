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

from nic import Nic
from nic_sim import NicSim

def parseCommandLine():
    import argparse
    parser = argparse.ArgumentParser(description="Run NDN-NIC simulation.")
    parser.add_argument("--comment", action="append",
                        help="ignored; may be used to identify running process")
    parser.add_argument("--bf1", type=int, default=1024,
                        help="BF1 size")
    parser.add_argument("--bf2", type=int, default=1024,
                        help="BF2 size")
    parser.add_argument("--bf3", type=int, default=1024,
                        help="BF3 size; 0 disables BF3, -1 disables BF3 and causes BF2 to ignore netType")
    parser.add_argument("--fib", default="NaiveFib",
                        help="FIB type or expression")
    parser.add_argument("--pit", default="NaivePit",
                        help="PIT type or expression")
    parser.add_argument("--cs", default="NaiveCs",
                        help="CS type or expression")
    args = parser.parse_args()
    return args

def makeTable(nic, arg):
    import table
    if '(' not in arg:
        return getattr(table, arg)
    return eval(arg, table.__dict__, dict(nic=nic))

def run(args):
    bf3, ignoreNetType2 = (None, True) if args.bf3 == -1 else (args.bf3, False)
    nic = Nic(args.bf1, args.bf2, bf3, ignoreNetType2=ignoreNetType2)
    fib = makeTable(nic, args.fib)
    pit = makeTable(nic, args.pit)
    cs = makeTable(nic, args.cs)
    nicSim = NicSim(nic, fib=fib, pit=pit, cs=cs)
    nicSim.processTtt(sys.stdin, sys.stdout)

if __name__ == "__main__":
    args = parseCommandLine()
    run(args)
