# coding=utf-8
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
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
        self.addLink(file_server1, switch1) # interface unycast
        self.addLink(file_server1,switch1) #interface anycast (configurada posteriormente)
        self.addLink(file_server2,switch1)
        self.addLink(file_server2,switch1)
        self.addLink(switch1,switch2)
        self.addLink(switch1,switch4)
        self.addLink(switch2,switch3)
        self.addLink(switch2,switch5)
        self.addLink(switch3,switch6)
        self.addLink(switch3,dns_server1) # interface unycast
        self.addLink(switch3,dns_server1) #interface anycast (configurada posteriormente)
        self.addLink(switch4,switch5)
        self.addLink(switch4,switch7)
        self.addLink(switch5,switch6)
        self.addLink(switch5,switch8)
        self.addLink(switch6,switch9)
        self.addLink(switch7,switch8)
        self.addLink(switch7,dns_server2) # interface unycast
        self.addLink(switch7,dns_server2) #interface anycast (configurada posteriormente)
        self.addLink(switch8,switch9)
        self.addLink(client1,switch2)
        self.addLink(client2,switch9)

def runMyTopo():

    topo = MyTopo()

    net = Mininet(
        topo = topo,
        controller = lambda name: RemoteController(name,ip='172.17.0.1')
    )

    fs1 = net.get('f1')
    fs1.setIP('10.0.0.250', intf='f1-eth1')
    fs1.setMAC('00:00:00:00:00:02',intf='f1-eth1')
    

    fs2 = net.get('f2')
    fs2.setIP('10.0.0.250', intf='f2-eth1')
    fs2.setMAC('00:00:00:00:00:04',intf='f2-eth1')

    d1 = net.get('d1')
    d1.setIP('10.0.0.251', intf='d1-eth1')
    d1.setMAC('00:00:00:00:01:02', intf='d1-eth1')

    d2 = net.get('d2')
    d2.setIP('10.0.0.251', intf='d2-eth1')
    d2.setMAC('00:00:00:00:01:04', intf='d2-eth1')

    c1 = net.get('c1')
    c1.setARP('10.0.0.250','ff:ff:ff:ff:ff:ff')
    c1.setARP('10.0.0.251','ff:ff:ff:ff:ff:ff')

    c2 = net.get('c2')
    c2.setARP('10.0.0.250','ff:ff:ff:ff:ff:ff')
    c2.setARP('10.0.0.251','ff:ff:ff:ff:ff:ff')

    net.start()

    CLI(net)

    net.stop()

if __name__ == '__main__':
    runMyTopo()

topos = { 'mytopo': (lambda : MyTopo())}
