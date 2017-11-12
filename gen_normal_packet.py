#!/usr/bin/env python27
import urllib2
import base64
import json
import os
import sys
import re
import scapy.all as scapy
from random import randint
import time

def send_packet():
  h_range = sys.argv[1]
  dst_addr = get_rand_dst(h_range)
  src_addr = get_rand_src()
  print("Send packet from: " + src_addr)
  print("\n to: " + dst_addr)
  scapy.send(scapy.IP(src=src_addr, dst=dst_addr))

def get_rand_dst(h_range):
  addr = ["10", "0", "0"]
  addr.append(str(randint(1, int(h_range))))
  return ".".join(addr)

def get_rand_src():
  addr = []
  for i in range(1,5):
    addr.append(str(randint(1, 254)))
  return ".".join(addr)

def get_sleep_time():
  ms = float(sys.argv[3])
  return ms / 1000.0

def gen_traffic():
  sleep_time = get_sleep_time()
  for i in range(1, int(sys.argv[2]) + 1):
    send_packet()
    time.sleep(sleep_time)

gen_traffic()
