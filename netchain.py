from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField, ByteField

class NetChain(Packet):
	name = "KeyValue"
	fields_desc = [
		LongField("preamble", 2),
		ByteField("mtype", 0),
		ByteField("dest" , 0),
		IntField("key", 0),
		IntField("value", 0),
	]

