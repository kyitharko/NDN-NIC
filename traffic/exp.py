#!/usr/bin/python2
"""Collect NDN-NIC Traffic and Table Trace."""

import atexit
import datetime
import functools
import time

from mininet.log import setLogLevel
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.cli import CLI

from mnndn.ndn import NdnHost
from mnndn.app import NdnPing,NdnPingServer

NDNNIC_FACEURI = 'udp4://224.0.23.170:56363'

def parseCommandLine():
    import argparse

    parser = argparse.ArgumentParser(description='Collect NDN-NIC Traffic and Table Trace.')
    parser.add_argument('--k', type=int, required=True,
                        help='count of hosts')
    parser.add_argument('--duration', type=int, default=60,
                        help='duration of emulation')
    parser.add_argument('--ping', action='append',
                        help='ping traffic client,host,interval,count')
    args = parser.parse_args()

    return args

def startPing(net, pings):
    print 'Start ping servers.'
    for host in net.hosts:
        server = NdnPingServer(host, '/%s' % host.name)
        server.start()
    time.sleep(1)

    print 'Start ping clients.'
    for pingConf in pings:
        clientHost, serverHost, interval, count = pingConf.split(',')
        client = NdnPing(net[clientHost], '/%s' % serverHost, interval=int(interval), count=int(count))
        client.start()

def run(args):
    topo = SingleSwitchTopo(k=args.k)
    net = Mininet(topo,
                  host=functools.partial(NdnHost, rout=None,
                       env=dict(
                         TTT_FACE=NDNNIC_FACEURI,
                         TTT_EPOCH=str(time.time()),
                         TTT_LOG='/var/log/ndn/ttt.log',
                       )))
    net.start()
    atexit.register(net.stop)

    print 'Start forwarding.'
    fws = [ host.getFw() for host in net.hosts ]
    for fw in fws:
        fw.start()
    time.sleep(5)

    for host in net.hosts:
        host.pexec('nfdc', 'register', '/', NDNNIC_FACEURI)

    if args.ping is not None:
        startPing(net, args.ping)

    startDt = datetime.datetime.now()
    endDt = startDt + datetime.timedelta(seconds=args.duration)
    print 'Run experiment, starting at %s, estimated ending at %s.' % (startDt, endDt)
    time.sleep(args.duration)

if __name__ == '__main__':
    setLogLevel('info')
    args = parseCommandLine()
    run(args)
