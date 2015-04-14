# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 14:47:35 2015

@author: jana
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time


connected_components = []
time_consumed = []

max_graph_size = 100

for size in range(max_graph_size):
    step_start = time.clock()
    print "current size: %d"%size
    probability = 2*np.log(size)/size
    temp = []
    for i in range(1000):
        G = nx.erdos_renyi_graph(size,probability)
        temp.append(len(nx.connected_components(G)))
    connected_components.append(np.asarray(temp).mean())
    step_stop = time.clock()
    time_consumed.append(step_stop - step_start)

fig, axes = plt.subplots(nrows=2, ncols=1)
ax1 = axes[0]
ax2 = axes[1]

axes[0].set_title('Average Number of connected components for\nan Erdos-Reiny-Graph'+\
'of size $n$ with $p=2\\ln(n)/n$')
ax1.set_ylabel('Number of connected components')
ax1.set_xlabel('Number of nodes in the graph $n$')    
ax1.plot((0, max_graph_size), (0, 0), 'k-')   
ax1.plot(connected_components,color='blue',linewidth=3,alpha=0.8)


ax2.set_title('Time to create an Erdos-Reiny-Graph of size $n$')
ax2.set_ylabel('Time t / [s]')
ax2.set_xlabel('Number of nodes in the graph $n$')
ax2.plot(time_consumed,color='FireBrick',linewidth=3,alpha=0.8)

fig.subplots_adjust(hspace=0.5)

plt.savefig("erdos_reiny_graph.pdf")

        