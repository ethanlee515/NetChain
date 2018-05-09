#!/usr/bin/env python

import route

commands = [list() for x in range(route.nb_switches)]

with open("commands.txt", "w+") as f:
	for key in range(route.max_key):
		head, body, tail = route.get_chain(key)
		p_head = "table_add process _put 2 1 " + str(head) + " " + str(key) + " => "
		p_head += str(route.getLoc(head, key)) + " " + str(body)
		commands[head - 1].append(p_head)
		
		p_body = "table_add process _put "
		p_body += "2 1 " + str(body) + " " + str(key) + " => "
		p_body += str(route.getLoc(body, key)) + " " + str(tail)
		commands[body - 1].append(p_body)

		locstr = str(route.getLoc(tail, key))

		p_tail = "table_add process _put "
		p_tail += "2 1 " + str(tail) + " " + str(key) + " => "
		p_tail += locstr + " 0"
		commands[tail - 1].append(p_tail)

		g_tail = "table_add process _get "
		g_tail += "2 0 " + str(tail) + " " + str(key) + " => "
		g_tail += locstr + " 0"
		commands[tail - 1].append(g_tail)

for i in range(route.nb_switches):
	with open("commands" + str(i + 1) + ".txt") as f:
		f.write("table_set_default process _nop\n")
		f.write("table_set_default route _drop\n")
		f.write("table_add route _route 2 =>")
		for command in commands[i]:
			f.write("\n" + command)

