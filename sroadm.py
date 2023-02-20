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

# class SingleROADMTopo(Topo):
#   def build(self):
#       "Build single ROADM topology"
#       # Packet network elements
#       hosts = [self.addHost(h) for h in ('h1', 'h2', 'h3')]
#       switches = [self.addSwitch(s)
#                   for s in ('s1', 's2', 's3')]
#       t1, t2, t3 = terminals = [
#           self.addSwitch(
#               t, cls=Terminal, transceivers=[('tx1',0*dBm,'C'), ('tx2',0*dBm,'C')],
#               monitor_mode='in')
#           for t in ('t1', 't2', 't3')]
#       r1 = self.addSwitch('r1', cls=ROADM)
#       # Ethernet links
#       for h, s, t in zip(hosts, switches, terminals):
#           self.addLink(h, s)
#           self.addLink(s, t, port2=1)
#       # WDM links
#       boost = ('boost', {'target_gain': 3.0*dB})
#       amp1 = ('amp1', {'target_gain': 25*.22*dB})
#       amp2 = ('amp2', {'target_gain': 25*.22*dB})
#       spans = [25*km, amp1, 25*km, amp2]
#       self.addLink(r1, t1, cls=OpticalLink, port1=1, port2=2,
#                    boost1=boost, spans=spans)
#       self.addLink(r1, t1, cls=OpticalLink, port1=2, port2=3,
#                    boost1=boost, spans=spans)
#       self.addLink(r1, t2, cls=OpticalLink, port1=3, port2=2,
#                    boost1=boost, spans=spans)
#       self.addLink(r1, t2, cls=OpticalLink, port1=4, port2=3,
#                    boost1=boost, spans=spans)
#       self.addLink(r1, t3, cls=OpticalLink, port1=5, port2=2,
#                    spans=[1.0*m])
#       self.addLink(r1, t3, cls=OpticalLink, port1=6, port2=3,
#                    spans=[1.0*m])


# class DoubleROADMTopo(Topo):
#     def build(self):
#         hosts = [self.addHost(h) for h in ('h1', 'h2', 'h3')]
#         switches = [self.addSwitch(s) for s in ('s1', 's2', 's3')]
#         t1, t2, t3 = terminals = [self.addSwitch(t, cls=Terminal, transceivers=[('tx1', 0*dBm, 'C')], monitor_mode='in') for t in ('t1', 't2', 't3')]
#         r1 = self.addSwitch('r1', cls=ROADM)
#         r2 = self.addSwitch('r2', cls=ROADM)
#         for h, s, t in zip(hosts, switches, terminals):
#             self.addLink(h, s)
#             self.addLink(s, t, port2=1)
#         boost = ('boost', {'target_gain': 3.0*dB})
#         amp1 = ('amp1', {'target_gain': 25*.22*dB})
#         amp2 = ('amp2', {'target_gain': 25*.22*dB})
#         spans = [25*km, amp1, 25*km, amp2]
#         self.addLink(r1, t1, cls=OpticalLink, port1=1, port2=2, boost1=boost, spans=spans)
#         self.addLink(r1, t2, cls=OpticalLink, port1=2, port2=2, boost1=boost, spans=spans)
#         self.addLink(r2, t3, cls=OpticalLink, port1=1, port2=2, spans=[1.0*m])
#         self.addLink(r1, r2, cls=OpticalLink, port1=3, port2=3, spans=[50*km])

class DoubleROADMTopo(Topo):
    def build(self):
        hosts = [self.addHost(h) for h in ('h1', 'h2', 'h3')]
        switches = [self.addSwitch(s) for s in ('s1', 's2', 's3')]
        t1, t2, t3 = terminals = [self.addSwitch(t, cls=Terminal, transceivers=[('tx1', 0*dBm, 'C'), ('tx2', 0*dBm, 'C')], monitor_mode='in') for t in ('t1', 't2', 't3')]
        r1 = self.addSwitch('r1', cls=ROADM)
        r2 = self.addSwitch('r2', cls=ROADM)
        for h, s, t in zip(hosts, switches, terminals):
            self.addLink(h, s)
            self.addLink(s, t, port2=1)
        boost = ('boost', {'target_gain': 3.0*dB})
        amp1 = ('amp1', {'target_gain': 25*.22*dB})
        amp2 = ('amp2', {'target_gain': 25*.22*dB})
        spans = [25*km, amp1, 25*km, amp2]
        self.addLink(r1, t1, cls=OpticalLink, port1=1, port2=2, boost1=boost, spans=spans)
        self.addLink(r1, t1, cls=OpticalLink, port1=2, port2=3, boost1=boost, spans=spans)
        self.addLink(r1, t2, cls=OpticalLink, port1=3, port2=2, boost1=boost, spans=spans)
        self.addLink(r1, t2, cls=OpticalLink, port1=4, port2=3, boost1=boost, spans=spans)
        self.addLink(r2, t3, cls=OpticalLink, port1=1, port2=2, spans=[1.0*m])
        self.addLink(r1, r2, cls=OpticalLink, port1=5, port2=5, spans=[50*km])

        
def plotNet(net, outfile="singleroadm.png", directed=False, layout='circo', colorMap=None, linksPerPair=5):
    try:
        import pygraphviz as pgv
    except:
        return
    color = {ROADM: 'red', Terminal: 'blue', OVSBridge: 'orange', Host: 'black'}
    if colorMap:
        color.update(colorMap)
    colors = {node: color.get(type(node), 'black') for node in net.values()}
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
        g.add_edge(node1.name, node2.name, headlabel=f' {node2}:{port2} ', taillabel=f' {node1}:{port1} ', labelfontsize=10, labelfontname='helvetica bold', penwidth=2)
    g.layout()
    g.draw(outfile)
def test(net):
    # Configure network and check connectivity
    info('*** Configuring network and checking connectivity')
    hosts = net.get('h1', 'h2')
    testdir = dirname(realpath(argv[0]))
    config_script = join(testdir, 'config-singleroadm.sh')
    run(config_script)
    assert net.ping(hosts, timeout=.5) == 0
    
    # Remove ROADM rule and check connectivity
    info('*** Removing ROADM rule and checking connectivity')
    remove_script = join(testdir, 'remove-singleroadm.sh')
    run(remove_script)
    assert net.ping(hosts, timeout=.5) == 100
    
def test(net):
    "Run config script and simple test"

    # Run the config script to configure the network
    info( '*** Configuring network\n')
    run('python3 config.py', shell=True)

    # Check connectivity between h1 and h2
    h1, h2 = net.get('h1', 'h2')
    info( f'*** Testing connectivity: {h1.IP()} -> {h2.IP()}\n')
    result = h1.cmd(f'ping -c5 {h2.IP()}')
    if '5 received' in result:
        info( 'Ping test: passed\n')
    else:
        info( 'Ping test: failed\n')


if __name__ == '__main__':

    cleanup()
    setLogLevel('info')

    topo = DoubleROADMTopo()
    net = Mininet(topo=topo, switch=OVSBridge, controller=None)
    restServer = RestServer(net)
    net.start()
    restServer.start()
    plotNet(net)
    test(net) if 'test' in argv else CLI(net)
    restServer.stop()
    net.stop()
