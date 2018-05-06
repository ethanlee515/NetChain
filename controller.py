#!/usr/bin/python

from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField, ByteField

import networkx as nx
import time
import sys
import threading

_THRIFT_BASE_PORT = 22222

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", required=True)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)
parser.add_argument('--cli', help='Path to BM CLI',
                    type=str, action="store", required=True)

args = parser.parse_args()

def handle_pkt(pkt):
	pkt = str(pkt)
	if len(pkt) != 22:
		return
	preamble = pkt[:8]
	if preamble != "\x00" * 7 + "\x02":
		return
	key = struct.unpack("!L", pkt[9:13])[0]

	# TODO insert stuff

	# TODO send the packet back

	
sniff(iface="eth0", prn=handle_pkt)

