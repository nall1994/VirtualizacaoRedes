package net.floodlightcontroller.bandwidthanalyzer;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Map;

import org.projectfloodlight.openflow.protocol.OFMessage;
import org.projectfloodlight.openflow.protocol.OFType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import net.floodlightcontroller.core.FloodlightContext;
import net.floodlightcontroller.core.IFloodlightProviderService;
import net.floodlightcontroller.core.IOFMessageListener;
import net.floodlightcontroller.core.IOFSwitch;
import net.floodlightcontroller.core.module.FloodlightModuleContext;
import net.floodlightcontroller.core.module.FloodlightModuleException;
import net.floodlightcontroller.core.module.IFloodlightModule;
import net.floodlightcontroller.core.module.IFloodlightService;
import net.floodlightcontroller.core.types.NodePortTuple;
import net.floodlightcontroller.statistics.IStatisticsService;
import net.floodlightcontroller.statistics.SwitchPortBandwidth;

public class BandwidthAnalyzer implements IOFMessageListener, IFloodlightModule {
	protected IFloodlightProviderService floodlightProvider;
	protected IStatisticsService statsProvider;
	protected static Logger logger;

	@Override
	public String getName() {
		return BandwidthAnalyzer.class.getSimpleName();
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
		statsProvider = context.getServiceImpl(IStatisticsService.class);
		logger = LoggerFactory.getLogger(BandwidthAnalyzer.class);
	}

	@Override
	public void startUp(FloodlightModuleContext context) throws FloodlightModuleException {
		floodlightProvider.addOFMessageListener(OFType.PACKET_IN,this);

	}

	@Override
	public Command receive(IOFSwitch sw, OFMessage msg, FloodlightContext cntx) {
		Map<NodePortTuple,SwitchPortBandwidth> statsMap = statsProvider.getBandwidthConsumption();
		for(Map.Entry<NodePortTuple, SwitchPortBandwidth> entry : statsMap.entrySet()) {
			System.out.println("ENTRY:");
			System.out.println("Node Port Tuple: ");
			System.out.println("Node: " + entry.getKey().getNodeId().toString());
			System.out.println("Port: " + entry.getKey().getPortId().toString());
			System.out.println("SwitchPortBandwidth: ");
			System.out.println("Switch: " + entry.getValue().getSwitchId().toString());
			System.out.println("Port: " + entry.getValue().getSwitchPort().toString());
			System.out.println("Bandwidth: " + entry.getValue().getLinkSpeedBitsPerSec().getValue());
		}
		
		return Command.CONTINUE;
	}

}
