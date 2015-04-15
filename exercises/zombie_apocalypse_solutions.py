import networkx as nx
import numpy as np
from numpy.random import random_integers
import matplotlib.pyplot as plt
plt.ioff()

size = 10

initial_condition = 'corner'



#hand-made two-dimensional grid graph
G = nx.empty_graph(size*size)
for i in range(size*size):
    #connect left
    if i%size != 0:
        G.add_edge(i,i-1)
    #connect right
    if i%size != size-1:
        G.add_edge(i,i+1)
    #connect up
    if i - size > 0:
        G.add_edge(i,i - size)
    #connect down
    if i + size < size*size:
        G.add_edge(i,i + size)
        
#add coordinates for plotting
for k in range(size):
    for l in range(size):
        G.node[k*size+l]['x'] = l
        G.node[k*size+l]['y'] = k
        
pos = {}
for k in G.node.keys():
    pos[k] = (G.node[k]['x'],G.node[k]['y'])

attr = {n:'human' for n in G.nodes()}        
nx.set_node_attributes(G,'creature',attr)

#initiate infection
def init(G,initial_condition):
    if initial_condition == 'edge':
        index = int(size/2)
        G.node[index]['creature'] = 'zombie'
    elif initial_condition == 'corner':
        index = 0
        G.node[index]['creature'] = 'zombie'
    elif initial_condition == 1:
        index = random_integers(0,size*size-1)
        G.node[index]['creature'] = 'zombie'
    elif initial_condition == 2:
        index1 = random_integers(0,size*size-1)
        index2 = random_integers(0,size*size-1)
        while index1 == index2:
            index2 = random_integers(0,size*size-1)
        G.node[index1]['creature'] = 'zombie'
        G.node[index2]['creature'] = 'zombie'
    else:
        indices = [random_integers(0,size*size-1) for j in range(initial_condition)]
        for index in indices:
            G.node[index]['creature'] = 'zombie'

#perform one infectuous step
def infection_step(G):
    for n in G.nodes():
        if G.node[n]['creature'] == 'zombie':
            for neighbor in G.neighbors(n):
                if np.random.rand() < p:
                    G.node[neighbor]['creature'] = 'zombie'

def plot(t):
    plt.clf()
    plt.title('Zombie Apocalypse')
    nx.draw_networkx_edges(G,pos=pos)
    infected = [n for n in G.nodes() if G.node[n]['creature'] == 'zombie']
    healthy = [n for n in G.nodes() if G.node[n]['creature'] == 'human']
    nx.draw_networkx_nodes(G,pos=pos,nodelist=healthy,\
            node_color='DarkSlateGray',alpha=0.6,node_size=200)
    nx.draw_networkx_nodes(G,pos=pos,nodelist=infected,\
            node_color='FireBrick',alpha=0.6,node_size=200)
    plt.savefig("apocalypse_%d.png"%t)
    

t = 0
p = 0.3
init(G,initial_condition)
humanity_alive = 'human' in nx.get_node_attributes(G,'creature').values()
while humanity_alive:
    if t%3 == 0:
        plot(t)
    infection_step(G)
    t += 1
    humanity_alive = 'human' in nx.get_node_attributes(G,'creature').values()
    
print "it took %d timesteps to destroy humanity"%t
        


    
        
    