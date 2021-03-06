# NIC Decision Log

A **NIC decision log** file logs decisions of NIC on incoming packets.  
It is the output of NIC simulator.

The file format is TAB separated values, where each line is a record, and columns are separated by TABs.  
Each record indicates the decision of NIC on an incoming packet.

## packet decision record

1.  timestamp, copied from packet arrival record
2.  network layer type, copied from packet arrival record
3.  NDN Name, copied from packet arrival record
4.  packet size, copied from packet arrival record
5.  decision of software forwarder, copied from packet arrival record
6.  decision of NIC; possible values are:
    * **DROP**: dropped
    * **FP-FIB**: accepted, BF-FIB Bloom filter false positive
    * **FP-CS**: accepted, BF-CS Bloom filter false positive
    * **FP-PIT**: accepted, BF-PIT Bloom filter false positive
    * **FIB**: accepted, BF-FIB key inserted by FIB
    * **PIT**: accepted, BF-PIT key inserted by PIT
    * **CS1**: accepted, BF-FIB key inserted by CS
    * **CS2**: accepted, BF-CS key inserted by CS
    * note: if there are multiple reasons for accepting a packet, list all reasons separated by comma, such as `FIB,CS1`
