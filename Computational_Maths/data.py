def rng(x):
	
	"""
	Random number generator (LCG).
	Parameters from C++11's 'minstd_rand'.
	"""

	m = 2**31 - 1
	a = 48271
	c = 0
	return (a*x + c)%m



def create_graph(id):

	"""
	Outputs a NetworkX graph object. 
	Input should be your 9-digit student ID.
	"""

	import numpy as np
	import networkx as nx

	# seed the rng
	seed = id

	# set base number of nodes and minimum number of edges
	n = 50
	e = 100

	# randomise number of nodes
	pm1 = (-1)**(seed % 2)
	seed = rng(seed)
	n += pm1*(seed % 11)
	seed = rng(seed)

	# randomise minimum number of edges
	pm2 = (-1)**(seed % 2)
	seed = rng(seed)
	e = 2*n + pm2*(seed % 11)
	seed = rng(seed)

	# initialise empty graph
	G = nx.convert_node_labels_to_integers(nx.empty_graph(n))

	# add e random edges before checking connectedness
	while G.number_of_edges() < e:
		node1 = seed % n
		seed = rng(seed)
		node2 = seed % n
		seed = rng(seed)
		if node1 != node2:
			if node2 > node1:
				node1, node2 = node2, node1
			G.add_edge(node1, node2)

	# if G is disconnected, find connected components and add edges
	if not nx.is_connected(G):
		cc = sorted(list(nx.connected_components(G)))
		largest = cc[0]
		for i in range(len(cc)):
			if len(cc[i]) > len(largest):
				largest = cc[i]		
		for component in cc:
			if component != largest:
				node1 = list(component)[seed % len(component)]
				seed = rng(seed)
				node2 = list(largest)[seed % len(largest)]
				seed = rng(seed)
				if node2 > node1:
					node1, node2 = node2, node1
				G.add_edge(node1, node2)

	# if for some reason G is still disconnected, print a helpful error message
	if nx.is_connected(G):
		return G
	else:
		print("Sorry, failed to produce a connected graph :( Please contact one of your lecturers.")
	
