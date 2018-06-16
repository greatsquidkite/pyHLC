# pyHLC

# Setup
Requires Python library ZeroMQ

One system must have timekeeper.py running, all other systems use /node files
Nodes must each have a socket_list.txt consisting of their address on the first line
and addresses of all other systems (including timekeeper) on following, separate lines
