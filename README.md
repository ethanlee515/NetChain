# NetChain
Class project at Johns Hopkins University

Implement [Netchains](https://www.cs.jhu.edu/~xinjin/files/NSDI18_NetChain.pdf) using P4 and Python

1. Execute *run\_demo.sh* to start the Mininet CLI
2. Type *xterm h1* (you can substitute h1 with h2 or h3)
3. Execute *kv.py h1* on the xterm (again, substituting h1 with whatever host you're using).

Dr. Jin said during his office hour on May 8 to insert the keys in initialization time,
since doing otherwise is difficult with how Mininet emulator is set up.
As a result, only keys between 0 to 199 are supported, so that starting up the demo wouldn't take a long time.

Didn't do the switch failure detection/recovery part.

File descriptions
+ make\_commands.py: Used to generate the command text files. Can be executed without command line arguments
+ route.py: Setting up NetChain. Near the top are the hard-coded values of max\_key and nb\_vnodes that can be changed if needed. If they are changed, make\_commands.py needs to be re-executed.
+ topo.txt: The network setup
+ topo.py: I've added a couple lines to make it so that different switches receive different commands.
+ kv.py: Sending and receiving packets that interacts with the NetChain key-value store.
+ run\_demo.sh: I was given this file from other parts of the assignment and I didn't touch it.
+ p4src/source\_routing.p4: P4 code that controls the router

