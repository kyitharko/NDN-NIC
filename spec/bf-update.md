# BF Update Log

A **BF update log** file logs hardware Bloom filter update counters for table changes.  
It is the output of NIC simulator.

The file format is TAB separated values, where each line is a record, and columns are separated by TABs.  
Each record records hardware BF updates for a table change.

## BF update record

1.  timestamp, copied from table change record
2.  change action, copied from table change record
3.  table, copied from table change record
4.  NDN Name, copied from table change record
5.  BF-FIB bits changed from 0 to 1
6.  BF-FIB bits changed from 1 to 0
7.  BF-CS bits changed from 0 to 1
8.  BF-CS bits changed from 1 to 0
9.  BF-PIT bits changed from 0 to 1
10. BF-PIT bits changed from 1 to 0
