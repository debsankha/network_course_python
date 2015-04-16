import numpy as np
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
plt.ion()

G = nx.erdos_renyi_graph(20,0.5)
fig = plt.figure(figsize=(8,8))
pos=nx.spring_layout(G)

src=np.random.choice(G.nodes())
allnodes=G.nodes()

nc=np.ones(G.number_of_nodes())
nc[allnodes.index(src)]=0


nodes = nx.draw_networkx_nodes(G,pos,node_color=nc)
edges = nx.draw_networkx_edges(G,pos) 


def update(n):
        global src
        nc=np.ones(G.number_of_nodes())
        src=np.random.choice(G.neighbors(src))
        nc[allnodes.index(src)]=0
        nodes.set_array(nc)
        return nodes,

anim = FuncAnimation(fig, update, interval=1000, blit=True)

input()
