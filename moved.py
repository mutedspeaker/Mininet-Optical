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
import subprocess
'''

 h1 - s1 - (t1,t2,t3,t4,t5) - r1 -- r2 -- r3 -- (t10,t11,t12,t13,t14,15) - s3 - h3
				    ||
		             (t6,t7,t8,t9,t10)
				    ||
				    h2
'''
				    
class SingleROADMTopo(Topo):
    def build(self):
        h1, h2, h3= [self.addHost(f'h{i}') for i in range(1, 4)]
        s1, s2, s3 = [self.addSwitch(f's{i}') for i in range(1, 4)]
        t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15 = [
            self.addSwitch(f't{i}', cls=Terminal, transceivers=[('tx1', 0*dBm, 'C')],
            monitor_mode='in') for i in range(1, 16)]
        r1, r2, r3 = [self.addSwitch(f'r{i}', cls=ROADM) for i in range(1, 4)]
	
	
	# Wdm Links:
        boost = ('boost', {'target_gain': 3.0*dB})
        amp1 = ('amp1', {'target_gain': 25*.22*dB})
        amp2 = ('amp2', {'target_gain': 25*.22*dB})
        spans = [25*km, amp1, 25*km, amp2]
	 # Add links
        for src, dst in [(h1, s1), (h2, s2), (h3, s3)]:
	        self.addLink(src, dst)
        for src, dst in [(s1, t1),(s1, t2),(s1, t3),(s1, t4),(s1, t5), (s2, t6),(s2, t7),(s2, t8),(s2, t9),(s2, t10), (s3, t11), (s3, t12), (s3, t13), (s3, t14), (s3, t15)]:
	        self.addLink(src, dst, port2=1)

        # Connections between routers and terminals
        for i in range(1, 6):
        	self.addLink(r1, locals()['t'+str(i)], cls=OpticalLink, port1=i+2, port2=i+2, boost1=boost, spans=spans)
        for i in range(6, 11):
               	self.addLink(r2, locals()['t'+str(i)], cls=OpticalLink, port1=i+2, port2=i+2, boost1=boost, spans=spans)
        for i in range(11, 16):
                self.addLink(r3, locals()['t'+str(i)], cls=OpticalLink, port1=i+2, port2=i+2, boost1=boost, spans=spans)

	# Adding links between r1 and r2
        self.addLink(r1, r2, cls=OpticalLink, port1=30, port2=30, boost1=boost, spans=spans)
        self.addLink(r2, r1, cls=OpticalLink, port1=31, port2=31, boost1=boost, spans=spans)
	
	# Adding links between r2 and r3
        self.addLink(r2, r3, cls=OpticalLink, port1=40, port2=40, boost1=boost, spans=spans)
        self.addLink(r3, r2, cls=OpticalLink, port1=41, port2=41, boost1=boost, spans=spans)


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
    script_name = 'ifteenTs.sh'
    script_path = '/home/ojas/Desktop/mycode/' + script_name
    subprocess.call(['gnome-terminal','--', 'bash', '-c','./' + script_name + '; $SHELL'])
    plotNet(net)
    test(net) if 'test' in argv else CLI(net)
    restServer.stop()
    
    net.stop()
