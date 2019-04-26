from mininet.topo import Topo

class MyTopo(Topo):

    def build(self):

        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')

        self.addLink(host1,switch1)
        self.addLink(switch1,switch2)
        self.addLink(switch2,host2)
        self.addLink(switch2,host3)

topos = { 'mytopo': (lambda : MyTopo())}