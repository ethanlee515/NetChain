#!/usr/bin/env python

import route

locs = [[] for x in range(route.nb_switches)]

if __name__ == "__main__":
	with open("commands.txt", "w+") as f:
		f.write("table_set_default process _nop\n")
		f.write("table_set_default route _route")
		for key in range(route.max_key):
			head, body, tail = route.get_chain(key)
			f.write("\ntable_add process _put 2 1 " + str(head) + " " + str(key) + " => ")
			f.write(str(route.getLoc(head, key)) + " " + str(body))
			
			f.write("\ntable_add process _put ")
			f.write("2 1 " + str(body) + " " + str(key) + " => ")
			f.write(str(route.getLoc(body, key)) + " " + str(tail))

			locstr = str(route.getLoc(tail, key))
			f.write("\ntable_add process _put ")
			f.write("2 1 " + str(tail) + " " + str(key) + " => ")
			f.write(locstr + " 0")
			f.write("\ntable_add process _get ")
			f.write("2 0 " + str(tail) + " " + str(key) + " => ")
			f.write(locstr + " 0")
