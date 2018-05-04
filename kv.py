#!/usr/bin/python

from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField, ByteField

import networkx as nx
import time
import sys
import threading

class KeyValue(Packet):
	name = "KeyValue"
	fields_desc = [
		LongField("preamble", 0),
		IntField("num_valid", 0),
		ByteField("port", 0),
		ByteField("mtype", 0),
		IntField("key", 0),
		IntField("value", 0),
	]

def toInt(s):
	return (ord(s[0]) << 24) + (ord(s[1]) << 16) + (ord(s[2]) << 8) + ord(s[3])

def send_pkt():
	time.sleep(0.1)
	sys.stdout.flush()
	tokens = raw_input("What do you want to send: ").split()
	if len(tokens) == 2:
		if tokens[0] != "get":
			print "invalid format"
			sys.stdout.flush()
			send_pkt()
		else:
			try:
				p = KeyValue(preamble=1, key=int(tokens[1]))
				sendp(p, iface="eth0")
			except ValueError:
				print "invalid format"
				sys.stdout.flush()
				send_pkt()
	elif len(tokens) == 3:
		if tokens[0] != "put":
			print "invalid format"
			sys.stdout.flush()
			send_pkt()
		else:
			try:
				p = KeyValue(preamble=1, mtype=1, key=int(tokens[1]), value=int(tokens[2]))
				sendp(p, iface="eth0")
			except ValueError:
				print "invalid format"
				sys.stdout.flush()
				send_pkt()
	else:
		print "invalid format"
		sys.stdout.flush()
		send_pkt()

def handle_pkt(pkt):
	pkt = str(pkt)
	if len(pkt) != 22:
		return
	preamble = pkt[:8]
	if preamble != "\x00" * 7 + "\x01":
		return
	mtype = pkt[13]
	if mtype == "\x02":
		time.sleep(.1)
		print toInt(pkt[18:])
		sys.stdout.flush()
	if mtype == "\x02" or mtype == "\x03":
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


