# Traffic and Table Trace

A **traffic and table trace** file contains records of packet arrival and table changes on a single host.  
It is the output of trace generation tool, and the input of NIC simulator.

The file format is TAB separated values, where each line is a record, and columns are separated by TABs.  
Each record indicates either a packet arrival, or a table change.

## packet arrival record

A packet arrival record has the following columns:

1.  timestamp, represented as seconds since scenario starts, format is 0.000000
2.  fixed string **PKT**, indicates packet arrival
3.  network layer type of the packet; possible values are:
    * **I**: Interest
    * **D**: Data
4.  NDN Name of the packet, represented as a URI without "ndn:" prefix
5.  packet size in octets
6.  decision of software forwarder if delivered; possible values are:
    * **DROP**: dropped
    * **FIB**: accepted, Interest matching FIB
    * **PIT**: accepted, Data matching PIT
    * **CS**: accepted, Interest matching CS but not FIB

## table change record

A table change record has the following columns:

1.  timestamp, represented as seconds since scenario starts, format is 0.000000
2.  change action; possible values are:
    * **INS**: inserting to table
    * **DEL**: deleting from table
3.  table being changed; possible values are:
    * **FIB**: Forwarding Information Base
    * **PIT**: Pending Interest Table
    * **CS**: Content Store
4.  NDN Name of the table entry, represented as a URI without "ndn:" prefix
