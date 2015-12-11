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

import table
from nic import Nic
from nic_sim import NicSim

FIB_IMPLS = [ cls for cls in dir(table) if cls.endswith("Fib") ]
PIT_IMPLS = [ cls for cls in dir(table) if cls.endswith("Pit") ]
CS_IMPLS = [ cls for cls in dir(table) if cls.endswith("Cs") ]

def parseCommandLine():
    import argparse
    parser = argparse.ArgumentParser(description="Run NDN-NIC simulation.")
    parser.add_argument("--bf1", type=int, default=1024,
                        help="BF1 size")
    parser.add_argument("--bf2", type=int, default=1024,
                        help="BF2 size")
    parser.add_argument("--fib", choices=FIB_IMPLS, default="NaiveFib",
                        help="FIB type")
    parser.add_argument("--pit", choices=PIT_IMPLS, default="NaivePit",
                        help="PIT type")
    parser.add_argument("--cs", choices=CS_IMPLS, default="NaiveCs",
                        help="CS type")
    args = parser.parse_args()
    return args

def run(args):
    nic = Nic(args.bf1, args.bf2)
    fib = getattr(table, args.fib)
    pit = getattr(table, args.pit)
    cs = getattr(table, args.cs)
    nicSim = NicSim(nic, fib=fib, pit=pit, cs=cs)
    nicSim.processTtt(sys.stdin, sys.stdout)

if __name__ == "__main__":
    args = parseCommandLine()
    run(args)