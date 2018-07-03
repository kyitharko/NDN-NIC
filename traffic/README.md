# NDN-NIC traffic generation

This directory contains program to generate Traffic and Table Trace.

**exp.py** is a mnndn script that emulates several NDN hosts on a single broadcast media.
NDN hosts are connected via an Ethernet switch, and all communications use the UDP multicast face, so that every host can see all the traffic on the multicast group, which emulates the broadcast media.
**NFD-ttt.patch** is an NFD patch that allows NFD to write Traffic and Table Trace to a file.
This functionality can be enabled and configured via environment variables, described in ttt.hpp after applying the patch.

## Installation

1. Install ndn-cxx 0.5.1.
2. Install ndn-tools 0.4.0.
3. Fetch NFD 0.5.1, patch with `NFD-ttt.patch`, and install patched version.
4. Install [mnndn](https://github.com/yoursunny/mnndn/tree/ec5f4ea39688807eca9d106e3a6b8cf092e8c45f).

## Usage

Run **exp.py** to emulate the network and collect traces.

Example for ndnping traffic:

    # Emulate 4 hosts on a single broadcast media.
    # h1 is consumer only.
    # h2 is producer only.
    # h3 is both consumer and producer.
    # h4 is neither consumer nor producer.
    sudo PYTHONPATH=$HOME/mnndn ./exp.py --k 4 --duration 60 --traffic ping,100,500,/h3,h3,h1 --traffic ping,100,500,/h2,h2,h3

Example for NFS traffic (requires `nfs-trace-server` and `nfs-trace-client` installed):

    # Emulate 4 hosts on a single broadcast media.
    # h1 and h2 are NFS servers.
    # h3 and h4 are NFS clients.
    sudo PYTHONPATH=$HOME/mnndn ./exp.py --k 4 --duration 60 --traffic nfs,s:h1:/tmp/nfs-dataset/server1.paths,s:h2:/tmp/nfs-dataset/server2.paths,c:h3:h3:/tmp/nfs-dataset/0000-0010.client1.replay,c:h4:h4:/tmp/nfs-dataset/0000-0010.client2.replay

Collected traces are in `/tmp/mnndn/*/var/log/ndn/ttt.log`.
Timestamps in traces among different hosts are comparable.
