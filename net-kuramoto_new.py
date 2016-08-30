import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx

def initialize():
    global g, nextg
    g = nx.karate_club_graph()
    g.pos = nx.spring_layout(g)
    for i in g.nodes_iter():
        g.node[i]['theta'] = 2 * pi * random()
        g.node[i]['omega'] = 1. + uniform(-0.05, 0.05)
    nextg = g.copy()
    
def observe():
    global g, nextg
    cla()
    # nx.draw(g, cmap = cm.hsv, vmin = -1, vmax = 1,
    #         node_color = [sin(g.node[i]['theta']) for i in g.nodes_iter()],
    #         pos = g.pos)

    nx.draw(g, cmap = cm.hsv, vmin = -1, vmax = 1,
        # cmap = cm.binary, vmin = 0, vmax = 1,
            # node_color = [g.node[i]['theta'] for i in g.nodes_iter()], 
            node_color = [sin(g.node[i]['theta']) for i in g.nodes_iter()],
            pos = g.pos)
    # nx.draw_networkx_edges(g,pos=g.pos)
    nx.draw_networkx_nodes(g,pos=g.pos,cmap = cm.hsv, vmin = -1, vmax = 1,node_size=2000, node_color=[sin(g.node[i]['theta']) for i in g])#,alpha=.5) #nodelist=[i for i in g if i!=g.nodes()[0]],   if i !=g.nodes()[0]
    # nx.draw_networkx_nodes(g,cmap = cm.hsv, vmin = -1, vmax = 1,pos=g.pos,nodelist=[g.nodes()[0]],node_shape='s',node_size=2000,
    #     node_color='r')
    lab={i:'%.2f' %sin(g.node[i]['theta']) for i in g}
    nx.draw_networkx_labels(g,pos=g.pos,labels=lab,font_size=15)
 
alpha = 1 # coupling strength
Dt = .1 # 0.01 # Delta t

def update():
    global g, nextg
    for i in g.nodes_iter():
        theta_i = g.node[i]['theta']
        nextg.node[i]['theta'] = theta_i + (g.node[i]['omega'] + alpha * ( \
            sum(sin(g.node[j]['theta'] - theta_i) for j in g.neighbors(i)) \
            / g.degree(i))) * Dt
    g, nextg = nextg, g

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
