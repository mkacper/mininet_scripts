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
  a_range = int(argv[1])
  h_range = int(argv[2])
  packets = int(argv[3])
  p_interval = int(argv[4])

  system("echo '' > gen_power.sh")
  for i in range(1, a_range):
    system("echo 'h" + str(i) + " nohup python gen_normal_packet.py " + str(h_range) + " " + str(packets)
    + " " + str(p_interval) + " /dev/null 2>&1 &' >> gen_power.sh")

emptyNet()
