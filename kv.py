#!/usr/bin/python

from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField, ByteField
from netchain import NetChain
import networkx as nx
import time
import sys
import threading
import route

if len(sys.argv) != 2:
	print("usage: kv.py hostname")
	exit()

hostname = sys.argv[1]

def port_str(key):
	chain = route.get_chain(key) 
	switches = ["s" + str(switch)) for switch in chain]
	s = route.route(hostname, switches[0])
	s += route.route(switches[0], switches[1])
	s += route.route(switches[1], switches[2])
	s += route.route(switches[2], hostname)
	return s

def send_pkt():
	time.sleep(0.1)
	sys.stdout.flush()
	tokens = raw_input("What do you want to send: ").split()
	key = int(tokens[1])
	if tokens[0] == "get":
		p = NetChain(key=key) / port_str(key)
		sendp(p, iface="eth0")
	elif tokens[0] == "put":
		p = NetChain(mtype=1, key=key, value=int(tokens[2])) / port_str(key)
		sendp(p, iface="eth0")
	else:
		print("invalid input")
		send_pkt()

def handle_pkt(pkt):
	pkt = str(pkt)
	if len(pkt) != 19:
		return

	preamble = pkt[:8]
	if preamble != "\x00" * 7 + "\x02":
		return
	mtype = pkt[8]
	if mtype == "\x00":
		time.sleep(.1)
		print struct.unpack("!L", pkt[14:18])
		sys.stdout.flush()
	send_pkt()

t = threading.Thread(target=sniff,
	kwargs={"iface": "eth0",
		"prn": (lambda x: handle_pkt(x))
	}
)

t.daemon = True
t.start()
send_pkt()
while True:
	time.sleep(.05)


