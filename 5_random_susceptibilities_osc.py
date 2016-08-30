import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

def initialize():
    global g, nextg#,nodlest
    
    g = nx.karate_club_graph()
    # g = nx.florentine_families_graph()
    # g=nx.path_graph(12)
    # g=nx.cycle_graph(12)
    # g=nx.petersen_graph()

    g.pos=graphviz_layout(g)
    # g.pos = nx.spring_layout(g)   
    
    for i in g.nodes_iter():
        if i !=g.nodes()[0]:
            g.node[i]['state']=0.
            
    # Susceptibility coefficients chosen randomly:

            g.node[i]['alpha']=random()

        else:
            g.node[i]['state']=1#2*pi
            g.node[i]['alpha']=0.   
    # nod=nx.draw_networkx_nodes(g,pos=g.pos,node_color = [g.node[i]['state'] for i in g.nodes_iter()])
    # # print nod
    # plt.colorbar(nod) 
    nextg = g.copy()
    
def observe():
    global g, nextg,nodlest
    cla()
    nx.draw(g, cmap = cm.hsv, vmin = -1, vmax = 1,
        # cmap = cm.binary, vmin = 0, vmax = 1,
            node_color = [g.node[i]['state'] for i in g.nodes_iter()], 

            pos = g.pos)
    # nx.draw_networkx_edges(g,pos=g.pos)
    nx.draw_networkx_nodes(g,pos=g.pos,cmap = cm.hsv, vmin = -1, vmax = 1,nodelist=[i for i in g if i!=g.nodes()[0]],node_size=2000,node_color=[g.node[i]['state'] for i in g if i !=g.nodes()[0]])#,alpha=.5)

    nx.draw_networkx_nodes(g,cmap = cm.hsv, vmin = -1, vmax = 1,pos=g.pos,nodelist=[g.nodes()[0]],node_shape='s',node_size=2000,node_color='r')
    lab={i:'%.2f' %g.node[i]['state'] for i in g}
    nx.draw_networkx_labels(g,pos=g.pos,labels=lab,font_size=15)


# alpha = .9 # diffusion constant
# Dt = 1. # Delta t

def update():
    global g, nextg,nodlest
    for i in g.nodes_iter():
        if i ==g.nodes()[0]:
            nextg.node[i]['state'] =-g.node[i]['state']
            continue
        # ci = g.node[i]['state']
        al=g.node[i]['alpha']
        nextg.node[i]['state'] = (al/g.degree(i)) * ( sum(g.node[j]['state'] for j in g.neighbors(i)) ) 
        + (1 - al)*g.node[i]['state']
        # nextg.node[i]['state'] = (al/g.degree(i)) * ( sum(g.node[j]['state'] for j in g.neighbors(i)) ) #*Dt#- ci ) #* Dt
        print i, g.node[i]['state'], nextg.node[i]['state']
        # print i, (al/g.degree(i)) * ( sum(g.node[j]['state'] for j in g.neighbors(i)) )*Dt,(al/g.degree(i)) ,( sum(g.node[j]['state'] for j in g.neighbors(i)) )*Dt
        
    g, nextg = nextg, g
# fig=plt.figure()
# plt.colorbar(fig)
# plt.show()
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
