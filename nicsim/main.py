# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2015-2016 Regents of the University of Arizona
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
This is an integration test for nic_sim
param string inputFileName: the input file name
param string outputFileName: the output file name
"""

from nic_sim import NicSim
import sys

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "usage: main <inputFileName> <outputFileName>"
		exit(1)
	else:
		inputFileName = sys.argv[1]
		outputFileName = sys.argv[2]

	nicSim = NicSim(100)

	inputFile = open(inputFileName,"r")
	outputFile = open(outputFileName,"w")

	c = 0
	for eachLine in inputFile:
		c+=1
		print "#"+str(c) +": "+eachLine
		outputList = nicSim.parseTrafficTableTrace(eachLine)
		if type(outputList) == type([]): 
			outputFile.writelines('\t'.join(outputList) +'\n')



	inputFile.close()
	outputFile.close()

