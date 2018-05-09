#!/usr/bin/python

from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField, ByteField
import struct
import networkx as nx
import time
import sys
import threading
import route

if len(sys.argv) != 2:
	print("usage: kv.py hostname")
	exit()

hostname = sys.argv[1]

class NetChain(Packet):
	name = "KeyValue"
	fields_desc = [
		LongField("preamble", 2),
		ByteField("mtype", 0),
		ByteField("dest" , 0),
		IntField("key", 0),
		IntField("value", 0),
	]

def send_pkt():
	time.sleep(0.1)
	sys.stdout.flush()
	tokens = raw_input("What do you want to send: ").split()
	key = int(tokens[1])
	if tokens[0] == "get":
		chain = route.get_chain(key)
		tail = "s" + str(chain[2])
		ports = route.route(hostname, tail)[1:] + route.route(tail, hostname)
		p = NetChain(dest=chain[2], key=key) / ports
		sendp(p, iface="eth0")
	elif tokens[0] == "put":
		chain = route.get_chain(key) 
		switches = ["s" + str(switch) for switch in chain]
		ports = route.route(hostname, switches[0])[1:]
		ports += route.route(switches[0], switches[1])
		ports += route.route(switches[1], switches[2])
		ports += route.route(switches[2], hostname)
		p = NetChain(mtype=1, dest=chain[0], key=key, value=int(tokens[2])) / ports
		sendp(p, iface="eth0")
	else:
		print("invalid input")
		send_pkt()

def handle_pkt(pkt):
	pkt = str(pkt)
	preamble = pkt[:8]
	if preamble != "\x00" * 7 + "\x02":
		return
	if pkt[9] != '\0':
		return
	mtype = pkt[8]
	if mtype == "\x00":
		time.sleep(.1)
		print struct.unpack("!L", pkt[14:18])[0]
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


