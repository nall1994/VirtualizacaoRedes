package net.floodlightcontroller.infoprinter;

import java.util.Collection;
import java.util.Map;

import org.projectfloodlight.openflow.protocol.OFMessage;
import org.projectfloodlight.openflow.protocol.OFType;

import net.floodlightcontroller.core.FloodlightContext;
import net.floodlightcontroller.core.IOFMessageListener;
import net.floodlightcontroller.core.IOFSwitch;
import net.floodlightcontroller.core.module.FloodlightModuleContext;
import net.floodlightcontroller.core.module.FloodlightModuleException;
import net.floodlightcontroller.core.module.IFloodlightModule;
import net.floodlightcontroller.core.module.IFloodlightService;
import net.floodlightcontroller.core.IFloodlightProviderService;
import java.util.ArrayList;
import java.util.concurrent.ConcurrentSkipListSet;
import java.util.Set;
import net.floodlightcontroller.packet.Ethernet;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class InfoPrinter implements IOFMessageListener, IFloodlightModule {
	protected IFloodlightProviderService floodlightProvider;
	protected Set<Long> macAddresses;
	protected static Logger logger;
	
	// Esta classe já está com o módulo implementado.
	// Agora é preciso arranjar forma de imprimir a seguinte informação:
	// 		- IP de origem e destino, protocolo de transporte e pacotes ARP com MAC destino e origem dos pacotes que passam no switch 1.
	// 		- Imprimir informação acerca da largura de banda. (usar iperf no terminal para criar fluxo de dados).

	@Override
	public String getName() {
		// TODO Auto-generated method stub
		
		return InfoPrinter.class.getSimpleName();
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
		// TODO Auto-generated method stub
		Collection<Class<? extends IFloodlightService>> l = new ArrayList<Class<? extends IFloodlightService>>();
		l.add(IFloodlightProviderService.class);
		
		return l;
	}

	@Override
	public void init(FloodlightModuleContext context) throws FloodlightModuleException {
		floodlightProvider = context.getServiceImpl(IFloodlightProviderService.class);
		macAddresses = new ConcurrentSkipListSet<Long>();
		logger = LoggerFactory.getLogger(InfoPrinter.class);
		// TODO Auto-generated method stub

	}

	@Override
	public void startUp(FloodlightModuleContext context) throws FloodlightModuleException {
		floodlightProvider.addOFMessageListener(OFType.PACKET_IN, this);
		// TODO Auto-generated method stub

	}

	@Override
	public Command receive(IOFSwitch sw, OFMessage msg, FloodlightContext cntx) {
		// TODO Auto-generated method stub
		Ethernet eth = IFloodlightProviderService.bcStore.get(cntx,IFloodlightProviderService.CONTEXT_PI_PAYLOAD);
		Long sourceMACHash = eth.getSourceMACAddress().getLong();
		if(!macAddresses.contains(sourceMACHash)) {
			macAddresses.add(sourceMACHash);
			String sma = eth.getSourceMACAddress().toString();
			String sid = sw.getId().toString();
			System.out.println("MAC: " + sma + " seen on switch: " + sid);
		}
		return Command.CONTINUE;
	}

}
