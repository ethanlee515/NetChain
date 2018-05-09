#!/usr/bin/python

from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField, ByteField
import argparse
import networkx as nx
import time
import sys
import threading
import route
import subprocess
import struct

_THRIFT_BASE_PORT = 22222

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", required=True)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)
parser.add_argument('--cli', help='Path to BM CLI',
                    type=str, action="store", required=True)

args = parser.parse_args()

nb_vNodes = 50

locs = [[] for x in range(route.nb_switches)]

def getLoc(switch, key):
	if key in locs[switch]:
		return locs[switch].index(key)
	else:
		locs[switch].append(key)
		return len(locs[switch]) - 1

def handle_pkt(pkt):
	pkt = str(pkt)
	preamble = pkt[:8]
	if preamble != "\x00" * 7 + "\x02":
		return
	key = struct.unpack("!L", pkt[10:14])[0]
	vNodes = route.getVNodes(key, nb_vNodes)
	head = route.getSwitch(vNodes[0], nb_vNodes)
	rep = route.getSwitch(vNodes[1], nb_vNodes)
	tail = route.getSwitch(vNodes[2], nb_vNodes)

	print ("inserting key: " + str(key))

	with open("command.txt", "w") as f:
		f.write("table_add process _put ")
		f.write("2 1 " + str(head) + " " + str(key) + " => ")
		f.write(str(getLoc(head, key)) + " " + str(rep))
	cmd = [args.cli, "--json", args.json,
		"--thrift-port", str(_THRIFT_BASE_PORT + head)]	
	with open("command.txt") as f:
		try:
			subprocess.check_output(cmd, stdin = f)
		except subprocess.CalledProcessError as e:
			print e.output
	with open("command.txt", "w") as f:
		f.write("table_add process _put ")
		f.write("2 1 " + str(rep) + " " + str(key) + " => ")
		f.write(str(getLoc(rep, key)) + " " + str(tail))
	cmd = [args.cli, "--json", args.json,
		"--thrift-port", str(_THRIFT_BASE_PORT + rep)]	
	with open("command.txt") as f:
		subprocess.check_output(cmd, stdin = f)

	with open("command.txt", "w") as f:
		locstr = str(getLoc(tail, key))
		f.write("table_add process _put ")
		f.write("2 1 " + str(tail) + " " + str(key) + " => ")
		f.write(locstr + " 0\n")
		f.write("table_add process _get ")
		f.write("2 0 " + str(tail) + " " + str(key) + " => ")
		f.write(locstr + " 0")
	cmd = [args.cli, "--json", args.json,
		"--thrift-port", str(_THRIFT_BASE_PORT + tail)]	
	with open("command.txt") as f:
		subprocess.check_output(cmd, stdin = f)

print("controlling now running")	
sniff(iface="eth0", prn=handle_pkt)

