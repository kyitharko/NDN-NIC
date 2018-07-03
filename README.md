# NDN-NIC

This repository contains programs and scripts for [NDN-NIC: Name-based Filtering on Network Interface Card](https://named-data.net/publications/ndn-nic/) research paper as well as NDN-NIC chapter in [Named Data Networking in Local Area Networks](http://hdl.handle.net/10150/625652) dissertation.
This code is provided for reproducibility purpose.
The author provides limited technical support on [ndn-interest mailing list](http://www.lists.cs.ucla.edu/pipermail/ndn-interest/).

## Code Organization

* [spec](spec/): file format specification.
* [traffic](traffic/): Mininet emulation script to generate Traffic and Table Trace from real traffic.
* [nicsim](nicsim/): Python simulator of NDN-NIC hardware and related software.
* [analyze](analyze/): analyze scripts.
* **param** branch: parameters used to generate the plots that appear in the dissertation chapter.

Related code:

* [nfsdump](https://github.com/yoursunny/nfsdump): NFS traffic collection.
* [sl-exp](https://bitbucket.org/yoursunny/sl-exp/src/master/): NFS traffic replay.
