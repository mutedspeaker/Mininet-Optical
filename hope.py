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
import os
import stat
import sys

def end():
    foo=raw_input()
    sys.exit()		

'''

 h1 - s1 - (t1,t2,t3,t4,t5) - r1 -- r2 -- r3 -- (t10,t11,t12,t13,t14,15) - s3 - h3
				    ||
		             (t6,t7,t8,t9,t10)
				    ||
				    h2
'''
def bash_text(n):
    
    a = ''
    a += "set -e\n"
    a += 'url="localhost:8080";\n'
#     a += 'declare -a t=() # declare an array\n'
#     a += 'for ((i=0;i<n;i++)); do\n'
#     a += '    t[i]=$url\n'
#     a += 'done\n'
    g = ''
    for i in range(1,n+1):
        g += f"t{i}=$url; "
    a += g 
    
    a += '\nr1=$url; r2=$url; r3=$url\n'
    a += 'curl="curl -s"\n'
    
    a += '\necho "* Configuring terminals in nRoadms.py network"\n'
    for i in range(1,n + 1):
        a += f'$curl "$t{i}/connect?node=t{i}&ethPort={i+2}&wdmPort={i+2}&channel={i*6}"\n'
    

    a += '\necho "* Resetting ROADM"\n'

    for i in range(1,4):
        a += f'$curl "$r{i}/reset?node=r{i}"\n'

    a += '\necho "* Configuring ROADM to connect r1,r2 and 4r3 to the respective terminals: "\n'

    for i in range(1,n//2 - 2):
        a += f'$curl "$r1/connect?node=r1&port1={i+2}&port2={i+2}&channels={i*6}"\n'
    for i in range(n //2 -2,n//2 + 2):
        a += f'$curl "$r2/connect?node=r2&port1={i+2}&port2={i+2}&channels={i*6}"\n'
    for i in range(n//2 + 2,n+1):
        a += f'$curl "$r3/connect?node=r3&port1={i+2}&port2={i+2}&channels={i*6}"\n'

    a += '\n$curl "$r1/connect?node=r1&port1=300&port2=300&channels=40"\n'
    a += '$curl "$r2/connect?node=r2&port1=310&port2=310&channels=40"\n'
    a += '$curl "$r2/connect?node=r2&port1=400&port2=400&channels=50"\n'
    a += '$curl "$r3/connect?node=r3&port1=410&port2=410&channels=50"\n'

    a += '''\n# turn on the roadm\n'''
    result = ""
    for i in range(1, n+1):
        command = '$curl "$t{}/turn_on?node=t{}"'.format(i, i)
        result += command + "\n"
    a += result
    
    result = ''
    for i in range(1, n+1):
        result += f't{i} '
    a += f"\nfor tname in {result}; do"
    a+= '''
    url=${!tname}
    $curl "$url/monitor?monitor=$tname-monitor"
done\n
    '''

    result = ''
    for i in range(1, n+1):
        result += f't{i} '
    a += f"\nfor tname in {result}; do"
    a+= '''
    url=${!tname}
    echo "* $tname"
    $curl "$url/monitor?monitor=$tname-monitor"
done\n'''

    a += 'echo "* 007 OUT!"\n'
    
    return a

def bash_creator(a):
    f= open("bash.sh","w+")
    f.write(a)
    f.close()
  
# class SingleROADMTopo(Topo):
#     def build(self):
#         h1, h2, h3= [self.addHost(f'h{i}') for i in range(1, 4)]
#         s = s1, s2, s3 = [self.addSwitch(f's{i}') for i in range(1, 4)]
#         t = [self.addSwitch(f't{i}', cls=Terminal, transceivers=[('tx1', 0*dBm, 'C')], monitor_mode='in') for i in range(n)]
#         r1, r2, r3 = [self.addSwitch(f'r{i}', cls=ROADM) for i in range(1, 4)]
	
	
# 	# Wdm Links:
#         boost = ('boost', {'target_gain': 3.0*dB})
#         amp1 = ('amp1', {'target_gain': 50*.22*dB})
#         amp2 = ('amp2', {'target_gain': 50*.22*dB})
#         spans = [50*km, amp1, 50*km, amp2]
# 	 # Add links
#         for src, dst in [(h1, s1), (h2, s2), (h3, s3)]:
# 	        self.addLink(src, dst)
# #         for src in s:
# #             for dst in t:
# #                 self.addLink(src, dst, port2=1)
#         for src, dst in [(s1, t[i]) for i in range(n//2 - 2)] + [(s2, t[i]) for i in range(n //2 -2, n//2 + 2)] + [(s3, t[i]) for i in range(n//2 + 2, n)]:
#             self.addLink(src, dst, port2=1)

#     # Connections between routers and terminals
#         for i in range(n//2 - 2):
#             self.addLink(r1, t[i], cls=OpticalLink, port1=i+3, port2=i+3, boost1=boost, spans=spans)

#         for i in range(n //2 -2, n//2 + 2):
#             self.addLink(r2, t[i], cls=OpticalLink, port1=i+3, port2=i+3, boost1=boost, spans=spans)

#         for i in range(n//2 + 2, n):
#             self.addLink(r3, t[i], cls=OpticalLink, port1=i+3, port2=i+3, boost1=boost, spans=spans)

# 	# Adding links between r1 and r2
#         self.addLink(r1, r2, cls=OpticalLink, port1=300, port2=300, boost1=boost, spans=spans)
#         self.addLink(r2, r1, cls=OpticalLink, port1=310, port2=310, boost1=boost, spans=spans)
	
# 	# Adding links between r2 and r3
#         self.addLink(r2, r3, cls=OpticalLink, port1=400, port2=400, boost1=boost, spans=spans)
#         self.addLink(r3, r2, cls=OpticalLink, port1=410, port2=410, boost1=boost, spans=spans)

class SingleROADMTopo(Topo):
    def build(self):
        h1, h2, h3= [self.addHost(f'h{i}') for i in range(1, 4)]
        s = s1, s2, s3 = [self.addSwitch(f's{i}') for i in range(1, 4)]

        # Generate variables t1 to tn and assign them to a list
        t_vars = [f"t{i}" for i in range(1, n+1)]

        # Use a list comprehension to create the switches and assign them to the t_vars
        t_vars = [self.addSwitch(t_var, cls=Terminal, transceivers=[('tx1', 0*dBm, 'C')], monitor_mode='in') for t_var in t_vars]
        
        r1, r2, r3 = [self.addSwitch(f'r{i}', cls=ROADM) for i in range(1, 4)]
        
        # Wdm Links:
        boost = ('boost', {'target_gain': 3.0*dB})
        amp1 = ('amp1', {'target_gain': 50*.22*dB})
        amp2 = ('amp2', {'target_gain': 50*.22*dB})
        spans = [50*km, amp1, 50*km, amp2]
        
        # Add links
        for src, dst in [(h1, s1), (h2, s2), (h3, s3)]:
            self.addLink(src, dst)
        
        for src, dst in [(s1, t_vars[i]) for i in range(n//2 - 2)] + [(s2, t_vars[i]) for i in range(n //2 -2, n//2 + 2)] + [(s3, t_vars[i]) for i in range(n//2 + 2, n)]:
                print(src, dst)
        
        for src, dst in [(s1, t_vars[i]) for i in range(n//2 - 2)] + [(s2, t_vars[i]) for i in range(n //2 -2, n//2 + 2)] + [(s3, t_vars[i]) for i in range(n//2 + 2, n)]:
            self.addLink(src, dst, port2=1)
        
        link_tuples = [(s1, t_vars[i]) for i in range(n//2 - 2)] + [(s2, t_vars[i]) for i in range(n //2 -2, n//2 + 2)] + [(s3, t_vars[i]) for i in range(n//2 + 2, n)]

        for src, dst in link_tuples:
            self.addLink(src, dst, port2=1)


        # Connections between routers and terminals
        for i in range(n//2 - 2):
            self.addLink(r1, t_vars[i], cls=OpticalLink, port1=i+2, port2=i+2, boost1=boost, spans=spans)

        for i in range(n //2 -2, n//2 + 2):
            self.addLink(r2, t_vars[i], cls=OpticalLink, port1=i+2, port2=i+2, boost1=boost, spans=spans)

        for i in range(n//2 + 2, n):
            self.addLink(r3, t_vars[i], cls=OpticalLink, port1=i+2, port2=i+2, boost1=boost, spans=spans)

        # Adding links between r1 and r2
        self.addLink(r1, r2, cls=OpticalLink, port1=300, port2=300, boost1=boost, spans=spans)
        self.addLink(r2, r1, cls=OpticalLink, port1=310, port2=310, boost1=boost, spans=spans)
    
        # Adding links between r2 and r3
        self.addLink(r2, r3, cls=OpticalLink, port1=400, port2=400, boost1=boost, spans=spans)
        self.addLink(r3, r2, cls=OpticalLink, port1=410, port2=410, boost1=boost, spans=spans)
	
# Debugging: Plot network graph
def plotNet(net, outfile="gConfignRoadms.png", directed=False, layout='circo',
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
    
    # for i in [20, 40]:
    # 	n = i
    # 	cleanup()
    # 	setLogLevel('info')

    # 	topo = SingleROADMTopo()
    # 	net = Mininet(topo=topo, switch=OVSBridge, controller=None)
    # 	restServer = RestServer(net)
    # 	net.start()
    # 	restServer.start()
    # 	a = bash_text(i)
    # 	bash_creator(a)	
    # 	st = os.stat('bash.sh')
    # 	os.chmod('bash.sh',st.st_mode | stat.S_IEXEC)  
    # 	script_name = 'bash.sh'
    # 	script_path = '/home/ojas/Desktop/mycode/' + script_name
    # 	subprocess.call(['gnome-terminal','--', 'bash', '-c','./' + script_name + '; $SHELL;'])
    # 	plotNet(net)
    # 	test(net) if 'test' in argv else CLI(net)
    # 	restServer.stop()
    # 	net.stop()

    n = 40
    i = 40
    cleanup()
    setLogLevel('info')

    topo = SingleROADMTopo()
    net = Mininet(topo=topo, switch=OVSBridge, controller=None)
    restServer = RestServer(net)
    net.start()
    restServer.start()
    a = bash_text(i)
    bash_creator(a)	
    st = os.stat('bash.sh')
    os.chmod('bash.sh',st.st_mode | stat.S_IEXEC)  
    script_name = 'bash.sh'
    script_path = '/home/ojas/Desktop/mycode/' + script_name
    subprocess.call(['gnome-terminal','--', 'bash', '-c','./' + script_name + '; $SHELL;'])
    plotNet(net)
    test(net) if 'test' in argv else CLI(net)
    restServer.stop()
    net.stop()
