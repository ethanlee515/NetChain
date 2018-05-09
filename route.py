#!/usr/bin/env python
import sys
import networkx as nx

links = []
with open("topo.txt", "r") as f:
	line = f.readline()[:-1]
	w, nb_switches = line.split()
	assert(w == "switches")
	line = f.readline()[:-1]
	w, nb_hosts = line.split()
	assert(w == "hosts")
	for line in f:
		if not f: break
		a, b = line.split()
		links.append( (a, b) )

nb_hosts = int(nb_hosts)
nb_switches = int(nb_switches)

port_map = {}

for a, b in links:
	if a not in port_map:
		port_map[a] = {}
	if b not in port_map:
		port_map[b] = {}
	assert(b not in port_map[a])
	assert(a not in port_map[b])
	port_map[a][b] = len(port_map[a]) + 1
	port_map[b][a] = len(port_map[b]) + 1

G = nx.Graph()
for a, b in links:
	G.add_edge(a, b)

shortest_paths = nx.shortest_path(G)

def route(src, dst):
	path = shortest_paths[src][dst]
	ret = ""
	first = path[1]
	for h in path[2:]:
		ret += chr(port_map[first][h])
		first = h
	return ret

# Converts a virtual node number to the switch it's assigned to.
# Probably suboptimal, but it gets the job done.
def getSwitch(vNode, nb_vNodes):
	r = nb_vNodes / nb_switches * nb_switches
	if vNode < r or nb_vNodes - r > 2:
		return vNode % nb_switches + 1
	else:
		return vNode - nb_vNodes + 4

# Converts a key to the corresponding virtual node number	
def getVNodes(key, nb_vNodes):
	x = (nb_vNodes * key / 10000) % nb_vNodes
	return [x, (x + 1) % nb_vNodes, (x + 2) % nb_vNodes]

