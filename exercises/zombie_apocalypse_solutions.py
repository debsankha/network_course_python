import networkx as nx
import numpy as np
from numpy.random import random_integers
import matplotlib.pyplot as plt
plt.ioff()

size = 10                       #size of the grid
m = 1                           #number of steps until the infection wars off
p = 0.4                         #infection probability
doctors_present = True          #are there doctors?
d = 5                           #number of doctors
initial_condition = 'corner'    #initial zombie starting point/number

def create_grid(size):
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
            
    return (G,pos)


#helper functions for setting zombies, doctors and humans
def set_zombie(G,index):
    G.node[index]['creature'] = 'zombie'
    G.node[index]['time_to_cure'] = m
        
def set_doctor(G,index):
    G.node[index]['creature'] = 'doctor'
    G.node[index]['time_to_cure'] = 0
    
def set_human(G,index):
    G.node[index]['creature'] = 'human'
    G.node[index]['time_to_cure'] = 0

#helper function to swap the attributes of two nodes    
def swap_places(G,index1,index2):
    temp_creature = G.node[index2]['creature']
    temp_time_to_cure = G.node[index2]['time_to_cure']
    G.node[index2]['creature'] = G.node[index1]['creature']
    G.node[index1]['creature'] = temp_creature
    G.node[index2]['time_to_cure'] = G.node[index1]['time_to_cure']
    G.node[index1]['time_to_cure'] = temp_time_to_cure
 
#helper function to check if a zombie is cured   
def check_cured(G):
    for n in G.nodes():
        if G.node[n]['time_to_cure'] == 0:
            G.node[n]['creature'] = 'human'

#initiate the grid
def init(G,initial_condition):
    attr = {n:'human' for n in G.nodes()}        
    nx.set_node_attributes(G,'creature',attr)
    attr = {n:0 for n in G.nodes()}        
    nx.set_node_attributes(G,'time_to_cure',attr)
    
    if initial_condition == 'edge':
        index = int(size/2)
        set_zombie(G,index)
    elif initial_condition == 'corner':
        index = 0
        set_zombie(G,index)                    
    elif initial_condition == 1:
        index = random_integers(0,size*size-1)
        set_zombie(G,index)
    elif initial_condition == 2:
        index1 = random_integers(0,size*size-1)
        index2 = random_integers(0,size*size-1)
        while index1 == index2:
            index2 = random_integers(0,size*size-1)
        set_zombie(G,index1)
        set_zombie(G,index2)
    else:
        indices = [random_integers(0,size*size-1) for j in range(initial_condition)]
        for index in indices:        
            set_zombie(G,index)
    
    if doctors_present:
        i = 0
        while i < d:
            index = np.random.random_integers(0,size*size - 1)
            if G.node[index]['creature'] == 'human':
                set_doctor(G,index)
                i += 1   

#perform one standard infectuous step
def infection_step(G):
    infected = [n for n in G.nodes() if G.node[n]['creature'] == 'zombie']
    for i in infected: 
        for neighbor in G.neighbors(i):
            if np.random.rand() < p:
                set_zombie(G,neighbor)
                
#perform one infectuous step with flying zombies
def infection_step_flying(G):
    infected = [n for n in G.nodes() if G.node[n]['creature'] == 'zombie']
    #select a random zombie
    random_zombie = infected[np.random.random_integers(0,len(infected) - 1)]
    #select a random tile at least size/2 edges away from the zombie 
    path_length = 0
    while path_length < size/2:
        target = np.random.random_integers(0,size*size - 1)
        path_length = len(nx.shortest_path(G,random_zombie,target))
    if np.random.rand() < p:
        set_zombie(G,target)
    
    for i in infected: 
        for neighbor in G.neighbors(i):
            if np.random.rand() < p:
                set_zombie(G,neighbor)

#perform one infectuous step with zombies self-curing after m steps                
def infection_step_self_curing(G):
    #first check if there are some cured zombies becoming human again
    check_cured(G)
    infected = [n for n in G.nodes() if G.node[n]['creature'] == 'zombie']
    for i in infected: 
        for neighbor in G.neighbors(i):
            if np.random.rand() < p and G.node[neighbor]['creature'] != 'zombie':
                set_zombie(G,neighbor)
    
    for i in infected:
        G.node[i]['time_to_cure'] -= 1

#perform one infectuous step with doctors moving randomly through the grid and
#curing zombies around them
def infection_step_doctors(G):
    #infect the healthy
    infected = [n for n in G.nodes() if G.node[n]['creature'] == 'zombie']
    for i in infected: 
        for neighbor in G.neighbors(i):
            if np.random.rand() < p and G.node[neighbor]['creature'] == 'human':
                set_zombie(G,neighbor)    
    
    #cure the infected
    doctors = [n for n in G.nodes() if G.node[n]['creature'] == 'doctor']
    for doctor in doctors:
        for neighbor in G.neighbors(doctor):
            if G.node[neighbor]['creature'] == 'zombie':
                set_human(G,neighbor)
                
    #move the doctors
    for doctor in doctors:
        neighbors = G.neighbors(doctor)
        target = np.random.random_integers(0,len(neighbors) - 1)
        swap_places(G,doctor,neighbors[target])
    
#function to plot the graph and save the image with a distinct filename
def plot(G,pos,t):
    plt.clf()
    plt.title('Zombie Apocalypse')
    nx.draw_networkx_edges(G,pos=pos)
    infected = [n for n in G.nodes() if G.node[n]['creature'] == 'zombie']
    healthy = [n for n in G.nodes() if G.node[n]['creature'] == 'human']
    doctors = [n for n in G.nodes() if G.node[n]['creature'] == 'doctor']
    
    nx.draw_networkx_nodes(G,pos=pos,nodelist=healthy,\
            node_color='DarkSlateGray',alpha=0.6,node_size=200)
    nx.draw_networkx_nodes(G,pos=pos,nodelist=infected,\
            node_color='FireBrick',alpha=0.6,node_size=200)
    nx.draw_networkx_nodes(G,pos=pos,nodelist=doctors,\
            node_color='ForestGreen',alpha=0.6,node_size=200)
            
    plt.savefig("apocalypse_%d.png"%t)
    

#create the graph
G,pos = create_grid()

#initialize the zombies/doctors on the graph
init(G,initial_condition)

#initialize break-conditions
humanity_alive = 'human' in nx.get_node_attributes(G,'creature').values()
zombiism_cured = 'zombie' not in nx.get_node_attributes(G,'creature').values()

#initialize time-step and time-step-hardcap
t = 0
hardcap = 100

#"main" loop
while humanity_alive and not zombiism_cured and hardcap > 0:
    print "infection step %d"%t
    
    #create a plot every 3 timesteps
    if t%3 == 0:
        plot(G,pos,t)
        
    #perform an infection step (use the step-function of choice here)
    infection_step_doctors(G)
    
    #increase timestep and update break conditions
    t += 1
    humanity_alive = 'human' in nx.get_node_attributes(G,'creature').values()
    zombiism_cured = 'zombie' not in nx.get_node_attributes(G,'creature').values()
    hardcap -= 1

#print final result
if humanity_alive == False:  
    print "it took %d timesteps to destroy humanity"%t
elif zombiism_cured == True:
    print "it took %d timesteps to cure zombiism"%t
else:
    print "hardcap for time-steps reached, aborting..."
        


    
        
    