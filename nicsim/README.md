# NDN-NIC simulator

This directory contains program to simulate NDN-NIC and related software.

Experiment programs are written to handle input and output files. 

nic_sim class contains one nic simulator and three tables, and it is in charge of 
parsing traffic table trace. For packet trace, nic_sim will invoke processPacket() 
method in nic simulator. For table modification trace, nic_sim will invoke related 
tables to handle. Eventually, both trafic and table trace are modifying the nic_bloom_filter

nic_sim
	- nic
		- nic_bloom_filter * 2
			- xor_hashes
	- PIT, FIB, CS tables
