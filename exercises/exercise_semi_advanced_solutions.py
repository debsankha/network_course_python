import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms import bipartite
import itertools as it
from os.path import join

### Shortest Paths and Cycles ###

print "***SHORTEST PATHS AND CYCLES ***"

#a) Loading the graph
dest = "/home/jana/PowerFolders/network_course_python/data/visualization"
file = "small_graph.gpickle"
G = nx.read_gpickle(join(dest,file))


#b) Count nodes and edges
nodes = len(G.nodes())
edges = len(G.edges())
print "b) The graph has %d nodes and %d edges\n"%(nodes,edges)

#c) Count the cycles
basis = nx.cycle_basis(G)
entry_length = [len(entry) for entry in basis]
print "c) The cycle basis of the graph contains %d entries, the longest entry contains %d edges.\n"\
%(len(basis),np.asarray(entry_length).max())


#d) Check for planarity
H = nx.Graph()
H.add_nodes_from([1,2,3,4,5])
H.add_edges_from([(1,2),(1,4),(2,3),(3,4),(3,5),(4,5)])

def is_planar(G):
    """
    function checks if graph G has K(5) or K(3,3) as minors,
    returns True /False on planarity and nodes of "bad_minor"
    """
    result=True
    n=len(G.nodes())
    if n>5:
        for subnodes in it.combinations(G.nodes(),6):
            subG=G.subgraph(subnodes)
            if bipartite.is_bipartite(G):# check if the graph G has a subgraph K(3,3)
                X, Y = bipartite.sets(G)
                if len(X)==3:
                    result=False

    if n>4 and result:
        for subnodes in it.combinations(G.nodes(),5):
            subG=G.subgraph(subnodes)
            if len(subG.edges())==10:# check if the graph G has a subgraph K(5)
                result=False

    return result

planar = is_planar(H)
if planar:    
    print "d) The graph is planar!\n"
else:
    print "d) The graph is not planar!\n"
    
#e) Shortest path between two nodes
node1 = np.random.random_integers(0,nodes)
node2 = np.random.random_integers(0,nodes)
path = nx.shortest_path(G, node1, node2)
print "e) The shortest path between node %d and node %d contains %d edges.\n"\
%(node1, node2, len(path))

#f) diameter of the graph
diameter = nx.diameter(G)
print "f) The diameter of the graph is %d.\n"%diameter 

#g) shortest path histograph
path_lengths = []
start = np.random.random_integers(0,nodes)
path_lengths = [len(nx.shortest_path(G,start,end)) for end in G.nodes()]

plt.title("Histogram of shortest paths from node %d to all other nodes"%start)
plt.xlabel("Path length / [number of edges]")
plt.ylabel("Counts")
plt.hist(path_lengths)
plt.show()

### Edge and Node Attributes ###
print "*** EDGE AND NODE ATTRIBUTES ***"
#a) attributes of the graph
node_attribute_dict = G.node[0]
edge_attribute_dict = G.edge[0][16]
print "a) The graph has the node attributes",node_attribute_dict.keys()
print "a) The graph has the edge attributes",edge_attribute_dict.keys()

#b) Total length of the graph
length = 0
for e in G.edges():
    x1 = G.node[e[0]]['x']
    x2 = G.node[e[1]]['x']
    y1 = G.node[e[0]]['y']
    y2 = G.node[e[1]]['y']
    length += np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
print "\nb) The total length of the graph is %d.\n"%length

#c) create a new attribute and use it for calculating the graphs length
for e in G.edges():
    x1 = G.node[e[0]]['x']
    x2 = G.node[e[1]]['x']
    y1 = G.node[e[0]]['y']
    y2 = G.node[e[1]]['y']
    length = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    G.edge[e[0]][e[1]].update({'length':length})
print "c) The graph has the edge attributes",edge_attribute_dict.keys()
    
length = 0
for e in G.edges(data=True):
    length += e[2]['length']

edge_attribute_dict = G.edge[0][16]    
print "c) The total length of the graph is %d.\n"%length

#d) histogram of edge lengths
edge_lengths = [e[2]['length'] for e in G.edges(data=True)]
plt.clf()
plt.xlabel("Edge length")
plt.ylabel("Counts")
plt.hist(edge_lengths,bins=20)
plt.show()
