#!/usr/bin/env python3

"""
singleroadm.py:
Simple optical network with three terminals connected to a
single ROADM in a "Y" topology. H1 can talk to either H2
or H3, depending on how the ROADM is configured.
"""

from mnoptical.dataplane import (Terminal, ROADM, OpticalLink,
                       OpticalNet as Mininet, km, m, dB, dBm)
from mnoptical.rest import RestServer
from mnoptical.ofcdemo.demolib import OpticalCLI as CLI

from mininet.node import OVSBridge, Host
from mininet.topo import Topo
from mininet.log import setLogLevel, warning, info
from mininet.clean import cleanup

from os.path import dirname, realpath, join
from subprocess import run
from sys import argv

class SingleROADMTopo(Topo):
    """
    h1 - s1 - t1 - r1 -- t2 -- r2 -- t3 -- r3 -- t4 - s2 - h2
    """
    def build(self):
        "Build multi ROADM topology"
        # Packet network elements
        h1, h2 = hosts = [self.addHost(h) for h in ('h1', 'h2')]
        s1, s2 = switches = [self.addSwitch(s)
                    for s in ('s1', 's2')]
        t1, t2, t3, t4 = terminals = [
            self.addSwitch(
                t, cls=Terminal, transceivers=[('tx1',0*dBm,'C')],
                monitor_mode='in')
            for t in ('t1', 't2', 't3', 't4')]
        r1 = self.addSwitch('r1', cls=ROADM)
        r2 = self.addSwitch('r2', cls=ROADM)
        r3 = self.addSwitch('r3', cls=ROADM)
#         # Ethernet links
#         for h, s, t in zip(hosts, switches, terminals):
#             self.addLink(h, s)
#             self.addLink(s, t, port2=1)
#             self.addLink(s, t, port2=4)
        self.addLink(h1, s1)
        self.addLink(s1, t1, port2=1)
        self.addLink(h2, s2)
        self.addLink(s2, t4, port2=1)
        # WDM links
        boost = ('boost', {'target_gain': 3.0*dB})
        amp1 = ('amp1', {'target_gain': 25*.22*dB})
        amp2 = ('amp2', {'target_gain': 25*.22*dB})
        spans = [25*km, amp1, 25*km, amp2]
        self.addLink(r1, t1, cls=OpticalLink, port1=13, port2=10,
                     boost1=boost, spans=spans)
        self.addLink(r1, t1, cls=OpticalLink, port1=14, port2=11,
                     boost1=boost, spans=spans)
                     
        self.addLink(r1, t2, cls=OpticalLink, port1=23, port2=20,
                     boost1=boost, spans=spans)
        self.addLink(r1, t2, cls=OpticalLink, port1=24, port2=21,
                     boost1=boost, spans=spans)

        self.addLink(r2, t2, cls=OpticalLink, port1=33, port2=30,
                     boost1=boost, spans=spans)
        self.addLink(r2, t2, cls=OpticalLink, port1=34, port2=31,
                     boost1=boost, spans=spans)
                     
        self.addLink(r2, t3, cls=OpticalLink, port1=43, port2=40,
                     boost1=boost, spans=spans)
        self.addLink(r2, t3, cls=OpticalLink, port1=44, port2=41,
                     boost1=boost, spans=spans)

        self.addLink(r3, t3, cls=OpticalLink, port1=53, port2=50,
                     boost1=boost, spans=spans)
        self.addLink(r3, t3, cls=OpticalLink, port1=54, port2=51,
                     boost1=boost, spans=spans)
                     
        self.addLink(r3, t4, cls=OpticalLink, port1=63, port2=60,
                     boost1=boost, spans=spans)
        self.addLink(r3, t4, cls=OpticalLink, port1=64, port2=61,
                     boost1=boost, spans=spans)

# Debugging: Plot network graph
def plotNet(net, outfile="gConfigThreeRoadms.png", directed=False, layout='circo',
            colorMap=None, linksPerPair=5):
    """Plot network graph to outfile
       linksPerPair: max # of links between a pair of nodes to plot, or
                     None for no limit (default: 5)"""
    try:
        import pygraphviz as pgv
    except:
        warning('*** Please install python3-pygraphviz for plotting\n')
        return
    color = {ROADM: 'red', Terminal: 'blue', OVSBridge: 'orange',
             Host: 'black'}
    if colorMap:
        color.update(colorMap)
    colors = {node: color.get(type(node), 'black')
              for node in net.values()}
    nfont = {'fontname': 'helvetica bold', 'penwidth': 3}
    g = pgv.AGraph(strict=False, directed=directed, layout=layout)
    roadms = [node for node in net.switches if isinstance(node, ROADM)]
    terms = [node for node in net.switches if isinstance(node, Terminal)]
    other = [node for node in net.switches if node not in set(roadms+terms)]
    for node in roadms + terms + other:
        g.add_node(node.name, color=colors[node], **nfont)
    for node in net.hosts:
        g.add_node(node.name, color=colors[node], **nfont, shape='box')
    linkcount = {}
    for link in net.links:
        intf1, intf2 = link.intf1, link.intf2
        node1, node2 = intf1.node, intf2.node
        port1, port2 = node1.ports[intf1], node2.ports[intf2]
        linkcount[node1,node2] = linkcount.get((node1, node2),0) + 1
        if linksPerPair is not None and linkcount[node1,node2] > linksPerPair:
            continue
        g.add_edge(node1.name, node2.name,
                   headlabel=f' {node2}:{port2} ',
                   taillabel=f' {node1}:{port1} ',
                   labelfontsize=10, labelfontname='helvetica bold',
                   penwidth=2)
    print("*** Plotting network topology to", outfile)
    g.layout()
    g.draw(outfile)

def test(net):
    "Run config script and simple test"
    info( '*** Configuring network and checking connectivity' )
    hosts = net.get( 'h1', 'h2' )
    testdir = dirname(realpath(argv[0]))
    script = join(testdir, 'config-singleroadm.sh')
    run(script)
    assert net.ping(hosts, timeout=.5) == 0
    info( '*** Removing ROADM rule and checking connectivity' )
    script = join(testdir, 'remove-singleroadm.sh')
    run(script)
    assert net.ping(hosts, timeout=.5) == 100

if __name__ == '__main__':

    cleanup()
    setLogLevel('info')

    topo = SingleROADMTopo()
    net = Mininet(topo=topo, switch=OVSBridge, controller=None)
    restServer = RestServer(net)
    net.start()
    restServer.start()
    plotNet(net)
    test(net) if 'test' in argv else CLI(net)
    restServer.stop()
    net.stop()
