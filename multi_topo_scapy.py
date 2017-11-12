#!/usr/bin/python                                                                            
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host
from mininet.node import OVSKernelSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from os import system
from sys import argv

def emptyNet():
  s_range = int(argv[1])
  h_range = int(argv[2])
  packets = int(argv[3])
  p_interval = float(argv[4])
  ddos_packets = int(argv[5])
  ddos_interval = int(argv[6])

  system("echo 'attacker python gen_ddos_packet.py target " + str(ddos_packets)
  + " " + str(ddos_interval) + " &' > gen_scapy.sh")
  system("echo 'h1 python gen_normal_packet.py " + str(h_range) + " " + str(packets)
  + " " + str(p_interval) + " &' >> gen_scapy.sh")
  net = Mininet(topo=None, controller=RemoteController, switch=OVSKernelSwitch,
                link=TCLink)
  c1 = net.addController('c1', controller=RemoteController, ip='192.168.56.1',
       port=6653)

  hosts = []
  switches = []
  h = 0
  for s in range(s_range):
    switches.append(net.addSwitch('s' + str(s), protocols='OpenFlow13'))
    for h in range(h + 1, h + 1 + h_range/s_range):
      hosts.append(net.addHost('h' + str(h)))
      net.addLink('s' + str(s), 'h' + str(h))

  for s in range(s_range - 1):
    net.addLink('s' + str(s), 's' + str(s+1))

  attacker = net.addHost('attacker')
  target = net.addHost('target')
  net.addLink('s0', 'attacker')
  net.addLink('s' + str(s_range - 1), 'target')

  net.start()

  CLI(net, script='gen_scapy.sh')
  CLI(net)

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    emptyNet()
