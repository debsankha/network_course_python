import networkx as nx
import numpy as np
import os
import matplotlib.pyplot as plt

size=100

#make sure we always use the same graph to make results comparable
graph_found = False
for file in os.listdir(os.getcwd()):
    if file == "power_law_cluster_graph.gpickle":
        graph_found = True
if not graph_found:
    #m = 2 and p = 0.6 seem to fit our needs
    G = nx.powerlaw_cluster_graph(size,2,0.6)
    nx.write_gpickle(G,"power_law_cluster_graph.gpickle")
else:
    G = nx.read_gpickle("power_law_cluster_graph.gpickle")

pos = nx.spring_layout(G,k=0.1)

#we try to find clusters by detecting nodes with an unusually high degree
#we define a cluster as each of these special nodes and their neighbors
#this already is an automatic way to identify clusters
degrees = nx.degree(G).values()
cluster_threshold = 2.5*np.asarray(degrees).mean()
clusters = []
for i,d in enumerate(degrees):
    if d > cluster_threshold:
        c = [i]
        c.extend(G.neighbors(i))
        clusters.append(c)

#we create a list of possible colors so we can assign a color to each cluster
#could also do this with a colormap to avoid an index error in the color_list
color_list = ['red','blue','green','yellow','purple','SkyBlue','maron',\
              'GoldenRod','salmon']

#we create a lookup table for the color of every node
#we also want to make nodes that do not belong to any cluster appear in gray
#and smaller than the nodes in the clusters
colors = ['gray']*len(G.nodes())
sizes = [100]*len(G.nodes())

for i,c in enumerate(clusters):
    color = color_list[i]
    for n in c:
        colors[n] = color
        sizes[n] = 300
    
#finally we draw the graph using the colors and sizes determined above 
#this way to color nodes still has the drawback that if a node belongs to
#more than one cluster, it will always be drawn with the color of the latest
#cluster to check. Maybe implement combination-colors for these nodes.
nx.draw_networkx(G, pos=pos, node_size=sizes, node_color=colors, \
                 font_size=8, alpha = 0.6)
plt.savefig("cluster_graph.pdf")

#define a function that performs a random walk from one node to one of
#its neighbors
def walk(node):
    neighbors = nx.neighbors(G,node)
    choose = np.random.random_integers(0,len(neighbors)-1)
    return neighbors[choose]

random = []
same = []

#randomly select two nodes in the graph 10000 times and record the time
#until the two walkers meet
for i in range(10000):
    n1 = np.random.random_integers(0,size-1)
    n2 = np.random.random_integers(0,size-1)
    while n2 == n1:
        n2 = np.random.random_integers(0,size-1)#
    j = 0
    while n1 != n2:
        n1 = walk(n1)
        n2 = walk(n2)
        j += 1
    random.append(j)
    
print "random selection done"
   
#randomly select a cluster and then randomly select two nodes both belonging to
#the same cluser. Record the time until the two walkers meet.
for i in range(10000):
    cluster = clusters[np.random.random_integers(0,len(clusters)-1)]
    n1 = cluster[np.random.random_integers(0,len(cluster)-1)]
    n2 = cluster[np.random.random_integers(0,len(cluster)-1)]
    while n2 == n1:
        n2 = cluster[np.random.random_integers(0,len(cluster)-1)]
    j = 0
    while n1 != n2:
        n1 = walk(n1)
        n2 = walk(n2)
        j += 1
    same.append(j)
    
print "same cluster selection done"

#trial and error shows that for around 10000 iterations one gets relatively
#consistent averages of steps needed until the two walkers meet
random_time = np.asarray(random).mean()
same_time = np.asarray(same).mean()
print "Steps until encounter for randomly selected nodes: %1.1f"%(random_time)
print "Steps until encounter for nodes from same cluster: %1.1f"%(same_time)

