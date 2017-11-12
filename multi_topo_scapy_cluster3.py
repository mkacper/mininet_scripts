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
  s_range = 3
  h_range = int(argv[1])
  packets = int(argv[2])
  p_interval = float(argv[3])
  c1addr = '192.168.56.1'
  c2addr = '192.168.56.100'
  c3addr = '192.168.56.103'

  system("echo 'h1 python gen_normal_packet.py " + str(h_range) + " " + str(packets)
  + " " + str(p_interval) + " &' > gen_scapy.sh")
  system("echo 'h" + str(h_range/3 + 1) +" python gen_normal_packet.py " + str(h_range) + " " + str(packets)
  + " " + str(p_interval) + " &' >> gen_scapy.sh")
  system("echo 'h'" + str(h_range) + " python gen_normal_packet.py " + str(h_range) + " " + str(packets)
  + " " + str(p_interval) + " &' >> gen_scapy.sh")
  net = Mininet(topo=None, controller=RemoteController, switch=OVSKernelSwitch,
                link=TCLink)
  c1 = net.addController('c1', controller=RemoteController, ip=c1addr,
       port=6653)
  c2 = net.addController('c2', controller=RemoteController, ip=c2addr,
       port=6653)
  c3 = net.addController('c3', controller=RemoteController, ip=c3addr,
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

  net.build()
  c1.start()
  c2.start()
  switches[0].start([c1])
  switches[1].start([c2])
  switches[2].start([c3])

  CLI(net, script='gen_scapy.sh')
  CLI(net)

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    emptyNet()
