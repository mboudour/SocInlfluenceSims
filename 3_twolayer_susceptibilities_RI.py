import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

# Susceptibility coefficients in two layers:

ls = 0.4
us = 0.94

def initialize():
    global g, nextg,nodlest

    g = nx.karate_club_graph()
    # g=nx.path_graph(12)
    # g=nx.cycle_graph(12)
    # g=nx.petersen_graph()
    # g = nx.florentine_families_graph()

    
    g.pos=graphviz_layout(g)
    # print nx.degree_centrality(g)
    # print nx.degree(g)

    for i in g.nodes_iter():
        if i !=g.nodes()[0]:
            g.node[i]['state']=random()
            g.node[i]['alpha'] = ls if random() < .5 else us
        else:
            g.node[i]['state']=1#2*pi
            g.node[i]['alpha']=0.
    
    lll=[]
    for i in g.nodes_iter():
        if g.node[i]['alpha'] == ls:
            lll.append(i)
    ull=[]
    for i in g.nodes_iter():
        if g.node[i]['alpha'] == us:
            ull.append(i)
    print 'lower susc', lll
    print 'upper susc', ull

    nodlest={}
    for nod in g.nodes():
        ap=g.node[nod]['alpha']
        if ap==0:
            nodlest[ap]=[nod]
        elif ap not in nodlest:
            nodlest[ap]=[nod]
        else:
            nodlest[ap].append(nod)
    nextg = g.copy()
    
    # plt.colorbar(sm)
    
def observe():
    global g, nextg,nodlest
    cla()
    nx.draw(g, cmap = cm.hsv, vmin = -1, vmax = 1,
        # cmap = cm.binary, vmin = 0, vmax = 1,
        # nodelist=[],pos = g.pos)
        node_color = [g.node[i]['state'] for i in g.nodes_iter()],pos = g.pos)
    nx.draw_networkx_edges(g,pos=g.pos)
    nodss={0:'s',ls:'d',us:'o'}
    # nodss={0:'v',.4:'s',0.94:'o'}
    for v,k in nodlest.items():
        nx.draw_networkx_nodes(g,pos=g.pos,nodelist=k,
            cmap = cm.hsv, vmin = -1, vmax = 1,
            # cmap = cm.binary, vmin = 0, vmax = 1,  
            node_shape=nodss[v],node_color=[g.node[i]['state'] for i in k])
        # nx.draw_networkx_nodes(g,pos=g.pos,nodelist=[g.nodes()[0]],node_shape='s',node_size=500,node_color='r')
        nx.draw_networkx_nodes(g,pos=g.pos,cmap = cm.hsv, vmin = -1, vmax = 1,nodelist=[i for i in g if i!=g.nodes()[0]],node_size=2000,node_color=[g.node[i]['state'] for i in g if i !=g.nodes()[0]])#,alpha=.5)
        nx.draw_networkx_nodes(g,cmap = cm.hsv, vmin = -1, vmax = 1,pos=g.pos,nodelist=[g.nodes()[0]],node_shape='s',node_size=2000,node_color='r')
        lab={i:'%.2f' %g.node[i]['state'] for i in g}
        nx.draw_networkx_labels(g,pos=g.pos,labels=lab,font_size=15)

# alpha = .9 # diffusion constant
# Dt = 1. # Delta t

def update():
    # sm = plt.cm.ScalarMappable(cmap=cm.hsv) #, norm=plt.normalize(vmin=-1, vmax=1))
    # sm._A = []
    # plt.colorbar(sm)
    global g, nextg,nodlest
    for i in g.nodes_iter():
        if i ==g.nodes()[0]:
            continue
        ci = g.node[i]['state']
        al=g.node[i]['alpha']
        nextg.node[i]['state'] = (al/g.degree(i)) * ( sum(g.node[j]['state'] for j in g.neighbors(i)) ) 
        + (1 - al)*g.node[i]['state']
        # nextg.node[i]['state'] = (al/g.degree(i)) * ( sum(g.node[j]['state'] 
        # for j in g.neighbors(i)) ) #*Dt#- ci ) #* Dt
        print i, g.node[i]['state'], nextg.node[i]['state']
        # print i, (al/g.degree(i)) * ( sum(g.node[j]['state'] for j in g.neighbors(i)) )*Dt,(al/g.degree(i)) ,( sum(g.node[j]['state'] for j in g.neighbors(i)) )*Dt
        
    g, nextg = nextg, g

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
