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
    h1 - s1 - t1 - r1 -- r2 -- r3 -- t3 - s3 - h3
    			 ||
    			 t2
    			 ||
    			 h3
    """
    def build(self):
        "Build multi ROADM topology"
        # Packet network elements
        h1, h2, h3 = hosts = [self.addHost(h) for h in ('h1', 'h2', 'h3')]
        s1, s2, s3 = switches = [self.addSwitch(s)
                    for s in ('s1', 's2', 's3')]
        t1, t2, t3 = terminals = [
            self.addSwitch(
                t, cls=Terminal, transceivers=[('tx1',0*dBm,'C')],
                monitor_mode='in')
            for t in ('t1', 't2', 't3')]
        r1, r2, r3 = roadms = [
            self.addSwitch(
                r, cls=ROADM)
            for r in ('r1', 'r2', 'r3')]
        # Ethernet links
        self.addLink(h1, s1)
        self.addLink(s1, t1, port2=1)
        
        self.addLink(h2, s2)       
        self.addLink(s2, t2, port2=1)
        
        self.addLink(h3, s3)
        self.addLink(s3, t3, port2=1)
        # WDM links
        boost = ('boost', {'target_gain': 3.0*dB})
        amp1 = ('amp1', {'target_gain': 25*.22*dB})
        amp2 = ('amp2', {'target_gain': 25*.22*dB})
        spans = [25*km, amp1, 25*km, amp2]
        self.addLink(r1, t1, cls=OpticalLink, port1=2, port2=2,
                     boost1=boost, spans=spans)
        self.addLink(r2, t2, cls=OpticalLink, port1=7, port2=7,
                     boost1=boost, spans=spans)        
        self.addLink(r1, r2, cls=OpticalLink, port1=3, port2=3,
                     boost1=boost, spans=spans)
        self.addLink(r2, r3, cls=OpticalLink, port1=4, port2=4,
                     boost1=boost, spans=spans)
        self.addLink(r3, t3, cls=OpticalLink, port1=5, port2=5,
                     boost1=boost, spans=spans)
                     
        # adding bidirection to it all
        self.addLink(r2, r1, cls=OpticalLink, port1=30, port2=30,
                     boost1=boost, spans=spans)
        self.addLink(r3, r2, cls=OpticalLink, port1=40, port2=40,
                     boost1=boost, spans=spans)
        # Connect all pairs of terminals
        #self.addLink(t1, t2)
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
