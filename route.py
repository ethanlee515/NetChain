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
nb_vnodes = 20
max_key = 200
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
	first = path[0]
	for h in path[1:]:
		ret += chr(port_map[first][h])
		first = h
	return ret

def get_switch(vNodeID):
	return (vNodeID * nb_switches / nb_vnodes) + 1

def hash(vNodeID):
	return (str(vNodeID * 127)).__hash__() % max_key

vnodes = [x for x in range(nb_vnodes)]
vnodes.sort(key=lambda x : hash(x))

# Converts a key to the corresponding virtual node number	
def get_chain(key):
	for i in range(len(vnodes)):
		if hash(vnodes[i]) > key:
			break
	i %= nb_vnodes
	head = get_switch(vnodes[i])
	while get_switch(vnodes[i]) == head:
		i = (i + 1) % nb_vnodes
	body = get_switch(vnodes[i])
	while get_switch(vnodes[i]) == head or get_switch(vnodes[i]) == body:
		i = (i + 1) % nb_vnodes
	tail = get_switch(vnodes[i])
	return (head, body, tail)	

_locs = [[] for x in range(nb_switches)]
for key in range(max_key):
	chain = get_chain(key)
	for switch in chain:
		_locs[switch - 1].append(key)

def getLoc(switch, key):
	return _locs[switch - 1].index(key)

if __name__ == "__main__":
	print(get_chain(33))
	print(get_chain(147))
	print(_locs)

