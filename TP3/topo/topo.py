# coding=utf-8
from mininet.topo import Topo
from mininet.link import Link
from mininet.node import Node
from mininet.node import Host
from mininet.node import Switch
from mininet.link import Intf

class MyTopo(Topo):

    def build(self):

        #Numeração dos switches vai de cima para baixo, da esquerda para a direita.
        #Switches
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')
        switch4 = self.addSwitch('s4')
        switch5 = self.addSwitch('s5')
        switch6 = self.addSwitch('s6')
        switch7 = self.addSwitch('s7')
        switch8 = self.addSwitch('s8')
        switch9 = self.addSwitch('s9')

        #Hosts (clientes, file servers e dns servers)
       

        client1 = self.addHost('c1',ip='10.0.0.14',mac='00:00:00:01:01:01')
        client2 = self.addHost('c2', ip='10.0.0.15',mac='00:00:00:01:01:02')
        file_server1 = self.addHost('f1',ip='10.0.0.10', mac='00:00:00:00:00:01')
        file_server2 = self.addHost('f2',ip='10.0.0.11', mac='00:00:00:00:00:03')
        dns_server1 = self.addHost('d1',ip='10.0.0.20', mac='00:00:00:00:01:01')
        dns_server2 = self.addHost('d2',ip='10.0.0.21', mac='00:00:00:00:01:03')

        #Links 
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
        self.addLink(client1,switch2)
        self.addLink(client2,switch9)

topos = { 'mytopo': (lambda : MyTopo())}
