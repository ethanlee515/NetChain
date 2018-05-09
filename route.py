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
nb_vnodes = 100
max_key = 10000
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

def getSwitch(vNodeID):
	return (vNodeID / nb_vnodes) + 1

def hash(vNodeID):
	return (str(vNodeID * 127)).__hash__() % max_key

vnodes = [x for x in range(nb_vnodes)]
vnodes.sort(key=lambda x : hash(x))


# Converts a key to the corresponding virtual node number	
def getVNodes(key):
	pass
	#TODO

if __name__ == "__main__":
	print vnodes
	for n in vnodes:
		print hash(n)
