import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

def initialize():
    global g, nextg,sources#,nodlest
    
    g = nx.karate_club_graph()
    # g = nx.florentine_families_graph()
    # g=nx.path_graph(12)
    # g=nx.cycle_graph(12)
    # g=nx.petersen_graph()

    g.pos=graphviz_layout(g)  
    # g.pos = nx.spring_layout(g) 

    sources=[g.nodes()[0],g.nodes()[33]]
    for i in g.nodes_iter():
        if i not in sources:
        # if i !=g.nodes()[0]:
            g.node[i]['state']=random()
            
    # Susceptibility coefficients chosen randomly:

            g.node[i]['alpha']=random()

        else:
            g.node[sources[0]]['state']=1.
            g.node[sources[0]]['alpha']=0.
            g.node[sources[1]]['state']=-1.
            g.node[sources[1]]['alpha']=0.
            # g.node[i]['state']=1.
            # g.node[i]['alpha']=0. 
    # nod=nx.draw_networkx_nodes(g,pos=g.pos,node_color = [g.node[i]['state'] for i in g.nodes_iter()])
    # # print nod
    # plt.colorbar(nod) 
    nextg = g.copy()
    
def observe():
    global g, nextg,nodlest,sources
    cla()
    nx.draw(g, cmap = cm.hsv, vmin = -1, vmax = 1,
        # cmap = cm.binary, vmin = 0, vmax = 1,
            node_color = [g.node[i]['state'] for i in g.nodes_iter()], 

            pos = g.pos)
    # nx.draw_networkx_edges(g,pos=g.pos)
    sources=[g.nodes()[0],g.nodes()[33]]
    nx.draw_networkx_nodes(g,pos=g.pos,cmap = cm.hsv, vmin = -1, vmax = 1,nodelist=[i for i in g if i not in sources],node_size=2000,node_color=[g.node[i]['state'] for i in g if i not in sources])#,alpha=.5)
    # !=g.nodes()[0]]
    nx.draw_networkx_nodes(g,cmap = cm.hsv, vmin = -1, vmax = 1,pos=g.pos,nodelist=sources,node_shape='s',node_size=2000,node_color='r')
    # [g.nodes()[0]]
    lab={i:'%.2f' %g.node[i]['state'] for i in g}
    nx.draw_networkx_labels(g,pos=g.pos,labels=lab,font_size=15)


# alpha = .9 # diffusion constant
# Dt = 1. # Delta t

def update():
    global g, nextg,nodlest,sources
    for i in g.nodes_iter():
        # if i ==g.nodes()[0]:
        #     nextg.node[i]['state'] =-g.node[i]['state']
        #     continue
        # if i in sources:
        if i ==sources[0] or i ==sources[1]:
            nextg.node[i]['state'] =-g.node[i]['state']
        # if i ==sources[1]:
        #     nextg.node[i]['state'] =-g.node[i]['state']
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
