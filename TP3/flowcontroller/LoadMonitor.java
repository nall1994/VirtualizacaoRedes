package net.floodlightcontroller.flowcontroller;

import java.io.IOException;
import java.lang.Thread;
import java.util.HashMap;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.rmi.UnknownHostException;
import java.net.DatagramPacket;

public class LoadMonitor extends Thread {
	private HashMap<String,Float> server_loads;
	DatagramSocket socket;
	
	public LoadMonitor() {
		server_loads = new HashMap<>();
		server_loads.put("f1",0.0f);
		server_loads.put("f2",0.0f);
		try {
			socket = new DatagramSocket(10001);
		} catch (SocketException e) {
			e.printStackTrace();
		}
	}
	
	
	public void run() {
		byte[] buf;
		byte[] buf_receive = new byte[256];
		String message = "LOAD_REQUEST";
		buf = message.getBytes();
		try {
			Thread.sleep(30000);
		}catch(InterruptedException ie) {
			ie.printStackTrace();
		}
		
		while(true) {
			try {
				InetAddress server_1_address = InetAddress.getByName("10.0.0.10");
				InetAddress server_2_address = InetAddress.getByName("10.0.0.11");
				DatagramPacket packet_1 = new DatagramPacket(buf,buf.length,server_1_address,10001);
				DatagramPacket packet_2 = new DatagramPacket(buf,buf.length,server_2_address,10001);
				socket.send(packet_1);
				System.out.println(packet_1.getAddress().toString());
				packet_1 = new DatagramPacket(buf_receive,buf_receive.length);
				socket.receive(packet_1);
				socket.send(packet_2);
				packet_2 = new DatagramPacket(buf_receive,buf_receive.length);
				socket.receive(packet_2);
				String value_1 = new String(packet_1.getData(), 0, packet_1.getLength());
				String value_2 = new String(packet_2.getData(), 0, packet_2.getLength());
				set_server_load("f1", Float.parseFloat(value_1));
				set_server_load("f2", Float.parseFloat(value_2));
				Thread.sleep(5000);
			} catch (java.net.UnknownHostException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			} catch(InterruptedException ie) {
				ie.printStackTrace();
			}
			
		}		
		
	}
	
	public void add_server(String server) {
		if(!server_loads.containsKey(server)) {
			server_loads.put(server,0.0f);
		}
	}
	
	public float get_server_load(String server) {
		float server_load = server_loads.get(server);
		return server_load;
	}
	
	public void set_server_load(String server,float new_load) {
		server_loads.replace(server,new_load);
	}
}
