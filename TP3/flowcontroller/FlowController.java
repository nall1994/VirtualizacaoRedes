package net.floodlightcontroller.flowcontroller;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import org.projectfloodlight.openflow.protocol.OFMessage;
import org.projectfloodlight.openflow.protocol.OFPacketOut;
import org.projectfloodlight.openflow.protocol.OFType;
import org.projectfloodlight.openflow.protocol.action.OFAction;
import org.projectfloodlight.openflow.types.ArpOpcode;
import org.projectfloodlight.openflow.types.EthType;
import org.projectfloodlight.openflow.types.IPv4Address;
import org.projectfloodlight.openflow.types.MacAddress;
import org.projectfloodlight.openflow.types.OFPort;

import net.floodlightcontroller.core.FloodlightContext;
import net.floodlightcontroller.core.IFloodlightProviderService;
import net.floodlightcontroller.core.IOFMessageListener;
import net.floodlightcontroller.core.IOFSwitch;
import net.floodlightcontroller.core.module.FloodlightModuleContext;
import net.floodlightcontroller.core.module.FloodlightModuleException;
import net.floodlightcontroller.core.module.IFloodlightModule;
import net.floodlightcontroller.core.module.IFloodlightService;
import net.floodlightcontroller.packet.ARP;
import net.floodlightcontroller.packet.Ethernet;
import net.floodlightcontroller.packet.IPv4;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FlowController implements IOFMessageListener, IFloodlightModule {
	protected IFloodlightProviderService floodlightProvider;
	protected static Logger logger;
	protected LoadMonitor load_monitor;
	protected String last_dns_server = "d2";

	@Override
	public String getName() {
		return FlowController.class.getSimpleName();
	}

	@Override
	public boolean isCallbackOrderingPrereq(OFType type, String name) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public boolean isCallbackOrderingPostreq(OFType type, String name) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public Collection<Class<? extends IFloodlightService>> getModuleServices() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Map<Class<? extends IFloodlightService>, IFloodlightService> getServiceImpls() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Collection<Class<? extends IFloodlightService>> getModuleDependencies() {
		Collection<Class<? extends IFloodlightService>> l = new ArrayList<Class<? extends IFloodlightService>>();
		l.add(IFloodlightProviderService.class);
		return l;
	}

	@Override
	public void init(FloodlightModuleContext context) throws FloodlightModuleException {
		floodlightProvider = context.getServiceImpl(IFloodlightProviderService.class);
		logger = LoggerFactory.getLogger(FlowController.class);
		load_monitor = new LoadMonitor();
		load_monitor.start();
		
	}

	@Override
	public void startUp(FloodlightModuleContext context) throws FloodlightModuleException {
		floodlightProvider.addOFMessageListener(OFType.PACKET_IN, this);

	}

	@Override
	public Command receive(IOFSwitch sw, OFMessage msg, FloodlightContext cntx) {
		//mandar pacotes para servidores para ver a carga.
		switch(msg.getType()) {
			
		case PACKET_IN:
			Ethernet eth = IFloodlightProviderService.bcStore.get(cntx,IFloodlightProviderService.CONTEXT_PI_PAYLOAD);
			if(eth.getEtherType() == EthType.IPv4) {
				IPv4 ipv4 = (IPv4) eth.getPayload();
				if((eth.getSourceMACAddress().toString().equals("00:00:00:01:01:01") || eth.getSourceMACAddress().toString().equals("00:00:00:01:01:02")) && eth.getDestinationMACAddress().toString().equals("ff:ff:ff:ff:ff:ff")) {
					if(ipv4.getDestinationAddress().toString().equals("10.0.0.250")) {
						float server_1_load = load_monitor.get_server_load("f1");
						float server_2_load = load_monitor.get_server_load("f2");
						Ethernet eth2 = (Ethernet) eth.clone();
						IPv4 ipv4_2 = (IPv4) ipv4.clone();
						if(server_1_load < server_2_load) {
							// Enviar pacote com o endereço MAC do servidor 1
							eth2.setDestinationMACAddress("00:00:00:00:00:02");
							System.out.println("Sending packet to server 1");
						} else {
							// Enviar pacote com o endereço MAC do servidor 2
							eth2.setDestinationMACAddress("00:00:00:00:00:04");
							System.out.println("Sending packet to server 2");
						}
						ipv4_2.setDestinationAddress("10.0.0.250");
						eth2.setPayload(ipv4_2);
						byte[] serialized = eth2.serialize();
						OFPacketOut pout = sw.getOFFactory().buildPacketOut()
															.setData(serialized)
															.setActions(Collections.singletonList((OFAction) sw.getOFFactory().actions().output(OFPort.FLOOD,0xffFFffFF)))
															.setInPort(OFPort.CONTROLLER)
															.build();
						sw.write(pout);
						return Command.STOP;
																	
						
					}
					if(ipv4.getDestinationAddress().toString().equals("10.0.0.251") && ipv4.getSourceAddress().toString().equals("10.0.0.14")) {
						Ethernet eth2 = (Ethernet) eth.clone();
						IPv4 ipv4_2 = (IPv4) ipv4.clone();
						System.out.println("Last DNS server used: " + last_dns_server);
						if(last_dns_server == "d1") {
							//Enviar para d2
							eth2.setDestinationMACAddress("00:00:00:00:01:04");
							last_dns_server = "d2";
							System.out.println("Sending packet to DNS server 2.");
						} else {
							//Enviar para d1
							eth2.setDestinationMACAddress("00:00:00:00:01:02");
							last_dns_server = "d1";
							System.out.println("Sending packet to DNS server 1.");
						}
						ipv4_2.setDestinationAddress("10.0.0.251");
						eth2.setPayload(ipv4_2);
						byte[] serialized = eth2.serialize();
						OFPacketOut pout = sw.getOFFactory().buildPacketOut()
														 .setData(serialized)
														 .setActions(Collections.singletonList((OFAction) sw.getOFFactory().actions().output(OFPort.FLOOD,0xffFFffFF)))
														 .setInPort(OFPort.CONTROLLER)
														 .build();
						
						sw.write(pout);
						return Command.STOP;
					} else if(ipv4.getDestinationAddress().toString().equals("10.0.0.251") && ipv4.getSourceAddress().toString().equals("10.0.0.15")) {
						Ethernet eth2 = (Ethernet) eth.clone();
						IPv4 ipv4_2 = (IPv4) ipv4.clone();
						eth2.setDestinationMACAddress("00:00:00:00:01:02");
						ipv4_2.setDestinationAddress("10.0.0.251");
						System.out.println("Client 2 asked. Sending packet for primary DNS server.");
						eth2.setPayload(ipv4_2);
						byte[] serialized = eth2.serialize();
						OFPacketOut pout = sw.getOFFactory().buildPacketOut()
														 .setData(serialized)
														 .setActions(Collections.singletonList((OFAction) sw.getOFFactory().actions().output(OFPort.FLOOD,0xffFFffFF)))
														 .setInPort(OFPort.CONTROLLER)
														 .build();
						
						sw.write(pout);
						return Command.STOP;
					} else {
						System.out.println(ipv4.getSourceAddress().toString());
						System.out.println(ipv4.getDestinationAddress().toString());
					}
				}
				
			} else if(eth.getEtherType() == EthType.ARP) {
				ARP arp = (ARP) eth.getPayload();
				if((arp.getTargetProtocolAddress().toString().equals("10.0.0.250") || arp.getTargetProtocolAddress().toString().equals("10.0.0.251")) && arp.getOpCode().toString().equals("1")) {
					Ethernet eth2 = (Ethernet) eth.clone();
					ARP arp_2 = new ARP();
					eth2.setSourceMACAddress(MacAddress.of("ff:ff:ff:ff:ff:ff"));
					arp_2.setSenderHardwareAddress(MacAddress.of("ff:ff:ff:ff:ff:ff"));
					System.out.println("ARP packet arrived! reassigning addresses");
					eth2.setDestinationMACAddress(arp.getSenderHardwareAddress());
					eth2.setEtherType(EthType.ARP);
					arp_2.setProtocolType(ARP.PROTO_TYPE_IP);
					arp_2.setHardwareType(ARP.HW_TYPE_ETHERNET);
					arp_2.setSenderProtocolAddress(IPv4Address.of(arp.getTargetProtocolAddress().toString()));
					arp_2.setTargetHardwareAddress(arp.getSenderHardwareAddress());
					arp_2.setTargetProtocolAddress(arp.getTargetProtocolAddress());
					arp_2.setOpCode(ArpOpcode.REPLY);
					arp_2.setHardwareAddressLength((byte) 0x06);
					arp_2.setProtocolAddressLength((byte) 0x04);
					eth2.setPayload(arp_2);
					
					byte[] serialized = eth2.serialize();
					OFPacketOut pout = sw.getOFFactory().buildPacketOut()
							 .setData(serialized)
							 .setActions(Collections.singletonList((OFAction) sw.getOFFactory().actions().output(OFPort.FLOOD,0xffFFffFF)))
							 .setInPort(OFPort.CONTROLLER)
							 .build();

					sw.write(pout);
					return Command.STOP;
							
				}
			}
			break;
		default:
			break;
		}
		return Command.CONTINUE;
	}

}
