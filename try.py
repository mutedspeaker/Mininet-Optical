class MultiROADMTopo(Topo):
    """
    h1 - s1 - t1 - r1 -- r2 -- r3 -- t11,t12,t13,t14,t15 - s11,s12,s13,s14,s15  - h11,h12,h13,h14,h15
                ||    ||
   t2,t3,t4,t5    t6,t7,t8,t9,t10
                ||    ||
 h2,h3,h4,h5    h6,h7,h8,h9,h10
    """
    def build(self):
        # Create hosts and switches
        hosts = [self.addHost(f"h{i}") for i in range(1, 16)]
        switches = [self.addSwitch(f"s{i}") for i in range(1, 16)]
        # Create terminals and roadms
        terminals = [self.addSwitch(f"t{i}", cls=Terminal, transceivers=[('tx1', 0*dBm, 'C')], monitor_mode='in') for i in range(1, 6)]
        roadms = [self.addSwitch(f"r{i}", cls=ROADM) for i in range(1, 4)]
        # Create links between hosts and switches
        for i in range(1, 6):
            self.addLink(hosts[i-1], switches[0])
        for i in range(6, 16):
            self.addLink(hosts[i-1], switches[i-5])
        # Create links between switches and terminals
        for i in range(1, 6):
            self.addLink(switches[i-1], terminals[i-1], port2=1)
        # Create links between terminals and roadms
        boost = ('boost', {'target_gain': 3.0*dB})
        amp1 = ('amp1', {'target_gain': 25*.22*dB})
        amp2 = ('amp2', {'target_gain': 25*.22*dB})
        spans = [25*km, amp1, 25*km, amp2]
        for i in range(1, 6):
            self.addLink(terminals[i-1], roadms[0], cls=OpticalLink, port1=i+1, port2=i+1, boost1=boost, spans=spans)
            self.addLink(terminals[i-1], roadms[1], cls=OpticalLink, port1=i+6, port2=i+6, boost1=boost, spans=spans)
        # Create links between roadms
        self.addLink(roadms[0], roadms[1], cls=OpticalLink, port1=3, port2=3, boost1=boost, spans=spans)
        self.addLink(roadms[1], roadms[2], cls=OpticalLink, port1=4, port2=4, boost1=boost, spans=spans)
        # Create links between switches and roadms
        for i in range(1, 6):
            self.addLink(switches[i-1], roadms[1], cls=OpticalLink, port1=i+10, port2=i+10, boost1=boost, spans=spans)
