#!/usr/bin/python2
"""Traffic patterns for experiment."""

import time

from mnndn.app import NdnPing,NdnPingServer

class Traffic:
    ARGUMENTS_DESCRIPTION = ''

    def start(self, net):
        """Start traffic."""
        raise NotImplementedError

    def stop(self, net):
        """Stop traffic immediately."""
        raise NotImplementedError

class PingTraffic(Traffic):
    ARGUMENTS_DESCRIPTION = '[interval,count,]/prefix,serverHost,clientHost,clientHost,..'

    def __init__(self, *opts):
        if len(opts) < 3:
            raise IndexError('PingTraffic needs at least /prefix,serverHost,clientHost')
        self.interval = NdnPing.DEFAULT_INTERVAL
        if opts[0][0] != '/':
            self.interval = int(opts[0])
            opts = opts[1:]
        self.count = None
        if opts[0][0] != '/':
            self.count = int(opts[0])
            opts = opts[1:]

        if len(opts) < 3:
            raise IndexError('PingTraffic needs at least /prefix,serverHost,clientHost')
        self.prefix = opts[0]
        self.serverHost = opts[1]
        self.clientHosts = opts[2:]

    def start(self, net):
        print 'Start ndnping server.'
        self.server = NdnPingServer(net[self.serverHost], self.prefix)
        self.server.start()
        time.sleep(1)

        print 'Start ndnping clients.'
        self.clients = {}
        for clientHost in self.clientHosts:
            self.clients[clientHost] = client = NdnPing(net[clientHost], self.prefix, interval=self.interval, count=self.count)
            client.start('/var/log/ndn/ndnping.log')

    def stop(self, net):
        print 'Stop ndnping clients.'
        for client in self.clients.itervalues():
            client.stop()
        time.sleep(1)

        print 'Stop ndnping server.'
        self.server.stop()

class NfsTraffic(Traffic):
    ARGUMENTS_DESCRIPTION = 's:serverHost:paths-file,..,c:clientHost:clientPrefix:client-name:ops-trace,..,rewrite-timestamp:t*2'

    def __init__(self, *opts):
        self.servers = {}
        self.clients = {}
        self.rewriteTimestamp = None

        addFuncs = {
          's': self.__addServer,
          'c': self.__addClient,
          'rewrite-timestamp': self.__setRewriteTimestamp
        }
        for opt in opts:
            opta = opt.split(':')
            addFunc = addFuncs.get(opta[0], None)
            if addFunc is None:
                raise TypeError
            addFunc(*opta[1:])

    def __addServer(self, host, pathsFile):
        self.servers[host] = dict(pathsFile=pathsFile)

    def __addClient(self, host, clientName, opsTrace):
        clientName = clientName.lstrip('/')
        self.clients[host] = dict(clientName=clientName, opsTrace=opsTrace)

    def __setRewriteTimestamp(self, expr):
        """Set an expression of 't' to rewrite the timestamp.
           This is passed to awk(1)."""
        self.rewriteTimestamp = expr

    def start(self, net):
        print 'Start NFS servers.'
        for hostName, d in self.servers.iteritems():
            host = net[hostName]
            d['proc'] = host.popen('nfs-trace-server', d['pathsFile'])
        time.sleep(3)

        print 'Start NFS clients.'
        for hostName, d in self.clients.iteritems():
            host = net[hostName]
            if self.rewriteTimestamp is None:
                cmd = 'nfs-trace-client %s < %s > %s' % (d['clientName'], d['opsTrace'], '/var/log/ndn/nfs-trace-client.log')
            else:
                cmd = 'awk \'BEGIN{FS=OFS=","}{t=$1;$1=%s;print}\' %s | nfs-trace-client %s > %s' % (
                      self.rewriteTimestamp, d['opsTrace'], d['clientName'], '/var/log/ndn/nfs-trace-client.log')
            d['proc'] = host.popen('bash', '-c', cmd)

    def stop(self, net):
        print 'Stop NFS clients.'
        for d in self.clients.itervalues():
            if 'proc' not in d:
                continue
            d['proc'].kill()
            d.pop('proc').wait()
        time.sleep(1)

        print 'Stop NFS servers.'
        for d in self.servers.itervalues():
            if 'proc' not in d:
                continue
            d['proc'].kill()
            d.pop('proc').wait()

TRAFFIC_CTORS = {
  'ping': PingTraffic,
  'nfs': NfsTraffic,
}

def makeTraffic(key, *opts):
    """Create traffic pattern from arguments."""
    cls = TRAFFIC_CTORS.get(key, None)
    if cls is None:
        raise KeyError('unknown traffic key')

    try:
        return cls(*opts)
    except TypeError:
        raise IndexError('traffic ' + key + ' expects arguments: ' + cls.ARGUMENTS_DESCRIPTION)
