from mininet.topo import Topo
from mininet.link import Link
from mininet.node import Host,Switch
from mininet.link import Intf

class MyTopo(Topo):

    def build(self):

        #Numeração dos switches vai de cima para baixo, da esquerda para a direita.
        #Switches
        switch1 = Switch('s1')
        switch2 = Switch('s2')
        switch3 = Switch('s3')
        switch4 = Switch('s4')
        switch5 = Switch('s5')
        switch6 = Switch('s6')
        switch7 = Switch('s7')
        switch8 = Switch('s8')
        switch9 = Switch('s9')
        '''
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')
        switch4 = self.addSwitch('s4')
        switch5 = self.addSwitch('s5')
        switch6 = self.addSwitch('s6')
        switch7 = self.addSwitch('s7')
        switch8 = self.addSwitch('s8')
        switch9 = self.addSwitch('s9')
        '''

        #Hosts (clientes, file servers e dns servers)
        intf_f1 = Intf('f1-eth1')
        intf_f1.setIP('10.0.0.250')
        intf_f1.setMAC('00:00:00:00:00:02')
        file_server1 = Host('f1')
        file_server1.setIP('10.0.0.10')
        file_server1.setMAC('00:00:00:00:00:01')
        file_server1.addIntf(intf_f1)
        self.addHost(file_server1)

        intf_f2 = Intf('f2-eth1')
        intf_f2.setIP('10.0.0.250')
        intf_f2.setMAC('00:00:00:00:00:4')
        file_server2 = Host('f2')
        file_server2.setIP('10.0.0.11')
        file_server2.setMAC('00:00:00:00:00:03')
        file_server2.addIntf(intf_f2)
        self.addHost(file_server2)

        intf_d1 = Intf('d1-eth1')
        intf_d1.setIP('10.0.0.251')
        intf_d1.setMAC('00:00:00:00:01:02')
        dns_server1 = Host('d1')
        dns_server1.setIP('10.0.0.12')
        dns_server1.setMAC('00:00:00:00:01:01')
        dns_server1.addIntf(intf_d1)
        self.addHost(dns_server1)

        intf_d2 = Intf('d2-eth1')
        intf_d2.setIP('10.0.0.251')
        intf_d2.setMAC('00:00:00:00:01:04')
        dns_server2 = Host('d2')
        dns_server2.setIP('10.0.0.13')
        dns_server2.setMAC('00:00:00:00:01:03')
        dns_server2.addIntf(intf_d2)
        self.addHost(dns_server2)

        client1 = self.addHost('c1',ip='10.0.0.14',mac='00:00:00:01:01:01')
        client2 = self.addHost('c2', ip='10.0.0.15',mac='00:00:00:01:01:02')

        '''
        file_server1 = self.addHost('fileServer1',ip='10.0.0.10', mac='00:00:00:00:00:10')
        file_server2 = self.addHost('fileServer2',ip='10.0.0.11', mac='00:00:00:00:00:11')
        dns_server1 = self.addHost('dnsServer1',ip='10.0.0.20', mac='00:00:00:00:00:20')
        dns_server2 = self.addHost('dnsServer2',ip='10.0.0.21', mac='00:00:00:00:00:21')
        client1 = self.addHost('client1',ip='10.0.0.30', mac='00:00:00:00:00:30')
        client2 = self.addHost('client2',ip='10.0.0.31', mac='00:00:00:00:00:31')
        '''

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
