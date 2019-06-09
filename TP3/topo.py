from mininet.topo import Topo

class MyTopo(topo):

    def build(self):

        # Numeração dos switches vai de cima para baixo, da esquerda para a direita.
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')
        switch4 = self.addSwitch('s4')
        switch5 = self.addSwitch('s5')
        switch6 = self.addSwitch('s6')
        switch7 = self.addSwitch('s7')
        switch8 = self.addSwitch('s8')
        switch9 = self.addSwitch('s9')
        file_server1 = self.addHost('fileServer1')
        file_server2 = self.addHost('fileServer2')
        dns_server1 = self.addHost('dnsServer1')
        dns_server2 = self.addHost('dnsServer2')

        self.addLink(file_server1, switch1)
        self.addLink(file_server2,switch1)
        self.addLink(switch1,switch2)
        self.addLink(switch1,switch4)
        self.addLink(switch2,switch3)
        self.addLink(switch2,switch5)
        self.addLink(switch3,switch6)
        self.addLink(switch3,dns_server1)
        self.addLink(switch4,switch5)
        self.addLink(switch5,switch6)
        self.addLink(switch5,switch8)
        self.addLink(switch6,switch9)
        self.addLink(switch7,switch8)
        self.addLink(switch7,dns_server2)
        self.addLink(switch8,switch9)

topos = { 'mytopo': (lambda : MyTopo())}
