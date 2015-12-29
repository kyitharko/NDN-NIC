# NDN-NIC traffic generation

This directory contains program to generate Traffic and Table Trace.

**exp.py** is a mnndn script that emulates several NDN hosts on a single broadcast media.
NDN hosts are connected via an Ethernet switch, and all communications use the UDP multicast face, so that every host can see all the traffic on the multicast group, which emulates the broadcast media.  
**NFD-ttt.patch** is an NFD patch that allows NFD to write Traffic and Table Trace to a file.
This functionality can be enabled and configured via environment variables, described in ttt.hpp after applying the patch.

## Installation

1. Install ndn-cxx 0.4.0-beta2.
2. Install ndn-tools latest, currently commit:3e79c9cd.
3. Fetch NFD 0.4.0-beta2, patch with `NFD-ttt.patch`, and install patched version.
4. Install [mnndn](http://github.com/yoursunny/mnndn).

## Usage

Run **exp.py** to emulate the network and collect traces.

Currently, only ndnping traffic is supported.
Example:

    # Emulate 4 hosts on a single broadcast media.
    # h1 is consumer only.
    # h2 is producer only.
    # h3 is both consumer and producer.
    # h4 is neither consumer nor producer.
    sudo PYTHONPATH=$HOME/mnndn ./exp.py --k 4 --duration 60 --traffic ping,100,500,/h3,h3,h1 --traffic ping,100,500,/h2,h2,h3

Collected traces are in `/tmp/mnndn/*/var/log/ndn/ttt.log`.
Timestamps in traces among different hosts are comparable.
