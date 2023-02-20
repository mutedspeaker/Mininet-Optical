from mnoptical.dataplane import Terminal, ROADM, OpticalLink, OpticalNet as Mininet, km, m, dB, dBm
from mininet.node import OVSBridge, Host
from mininet.topo import Topo

class SingleROADMTopo(Topo):
    def build(self):
        hosts = [self.addHost(h) for h in ('h1', 'h2', 'h3')]
        switches = [self.addSwitch(s) for s in ('s1', 's2', 's3')]
        t1, t2, t3 = terminals = [self.addSwitch(t, cls=Terminal, transceivers=[('tx1', 0*dBm, 'C')], monitor_mode='in') for t in ('t1', 't2', 't3')]
        r1 = self.addSwitch('r1', cls=ROADM)
        for h, s, t in zip(hosts, switches, terminals):
            self.addLink(h, s)
            self.addLink(s, t, port2=1)
        boost = ('boost', {'target_gain': 3.0*dB})
        amp1 = ('amp1', {'target_gain': 25*.22*dB})
        amp2 = ('amp2', {'target_gain': 25*.22*dB})
        spans = [25*km, amp1, 25*km, amp2]
        self.addLink(r1, t1, cls=OpticalLink, port1=1, port2=2, boost1=boost, spans=spans)
        self.addLink(r1, t2, cls=OpticalLink, port1=2, port2=2, boost1=boost, spans=spans)
        self.addLink(r1, t3, cls=OpticalLink, port1=3, port2=2, spans=[1.0*m])

def main():
    topo = SingleROADMTopo()
    net = Mininet(topo=topo, switch=OVSBridge)
    net.start()
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    main()
