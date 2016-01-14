#!/usr/bin/python2
"""Collect NDN-NIC Traffic and Table Trace."""

import atexit
import datetime
import functools
import threading
import time

from mininet.log import setLogLevel
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.cli import CLI

from mnndn.ndn import NdnHost, NfdForwarder
from mnndn.app import NdnPing, NdnPingServer

from exp_traffic import makeTraffic

NDNNIC_FACEURI = 'udp4://224.0.23.170:56363'

def parseCommandLine():
    import argparse

    parser = argparse.ArgumentParser(description='Collect NDN-NIC Traffic and Table Trace.')
    parser.add_argument('--k', type=int, required=True,
                        help='count of hosts')
    parser.add_argument('--duration', type=int, default=60,
                        help='duration of emulation')
    parser.add_argument('--traffic', action='append', required=True,
                        help='traffic configuration string')
    parser.add_argument('--cs', type=int, default=4096,
                        help='ContentStore capacity')
    args = parser.parse_args()

    return args

def run(args):
    topo = SingleSwitchTopo(k=args.k)
    net = Mininet(topo,
                  host=functools.partial(NdnHost,
                       fw=functools.partial(NfdForwarder, csCapacity=args.cs),
                       rout=None,
                       env=dict(
                         TTT_FACE=NDNNIC_FACEURI,
                         TTT_EPOCH=str(time.time()),
                         TTT_LOG='/var/log/ndn/ttt.log',
                       )))
    net.start()
    atexit.register(net.stop)

    traffics = [ makeTraffic(*trafficConfig.split(',')) for trafficConfig in args.traffic ]

    print 'Start forwarding.'
    fws = [ host.getFw() for host in net.hosts ]
    for fw in fws:
        fw.start()
    time.sleep(5)

    for host in net.hosts:
        host.pexec('nfdc', 'register', '/', NDNNIC_FACEURI)

    print 'Start traffic.'
    startTrafficThreads = [ threading.Thread(target=functools.partial(traffic.start, net)) for traffic in traffics ]
    [ thread.start() for thread in startTrafficThreads ]
    [ thread.join() for thread in startTrafficThreads ]

    startDt = datetime.datetime.now()
    endDt = startDt + datetime.timedelta(seconds=args.duration)
    print 'Run experiment, starting at %s, estimated ending at %s.' % (startDt, endDt)
    time.sleep(args.duration)

    print 'Stop traffic.'
    stopTrafficThreads = [ threading.Thread(target=functools.partial(traffic.stop, net)) for traffic in traffics ]
    [ thread.start() for thread in stopTrafficThreads ]
    [ thread.join() for thread in stopTrafficThreads ]
    time.sleep(1)

if __name__ == '__main__':
    setLogLevel('info')
    args = parseCommandLine()
    run(args)
