####FIRST POINT
#PARSE JSON FILE
import json

with open('reduced_dblp.json') as json_data:
    data = json.load(json_data)
#print (data) 
#CREATE NODES

authors=[]
for element in data:
    authors.append(element['authors'])
#print(authors)

author=[]
c=[]
for element in authors:
    a=[]
    for i in element:
        author.append(i['author_id'])
        a.append(i['author_id'])
    c.append(a)
#print(c)
#print(author)

default_value = None
nodes = dict.fromkeys(author,default_value)
#print(nodes)

#CREATE THE EDGES

for element in c:
    for k,v in nodes.items():
        if element[0]==k:
            if nodes[k]==None:
                if len(element)>1:
                    nodes[k]=element
            else:
                for i in element:
                    nodes[k].append(i)

for k,v in nodes.items():
    if v!=None:
        for element in v:
            if element==k:
                v.remove(element)    
#print (nodes)  
newNodes = dict((k, v) for k, v in nodes.items() if v != None)    
#print(newNodes)

#CREATE ADJACENCY MATRIX
import numpy as np
m=len(nodes)
A=np.zeros((m, m))
#print(A)

rows=columns=list(nodes.keys())
#print(rows)
for k,v in newNodes.items():
    for i in range(len(rows)):
        if k==rows[i]:
            for element in v:
                for j in range(len(columns)):
                    if element==columns[j]:
                        A[i][j]=1
                        A[j][i]=1
#print(A)

#CREATE WEIGHT MATRIX
#Create a dictionary with the publications of each author
default_value = None
b = dict.fromkeys(author,default_value)
#print(b)
for a in b.keys():
    for element in data:
        for i in element['authors']:
            if (a==i['author_id']):
                if (b[a]==None):
                    b[a]=[element['id_publication_int']]
                else:
                    b[a].append(element['id_publication_int'])
#print(b)    

#Create weight matrix
W=np.zeros((m,m))
for i in range(len(rows)):
    for j in range(len(columns)):
        if A[i][j]==1:
            author1=rows[i]
            author2=columns[j]
            elements1=set(b[author1])
            elements2=set(b[author2])
            union=elements1.union(elements2)
            inter=elements1.intersection(elements2)
            jaccard=len(inter)/len(union)
            W[i][j]=1-jaccard
        else:
            W[i][j]==1

#print(W)
#print(A)
#CREATE GRAPH
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import pylab

G = nx.Graph()

for i in range(m):
    for j in range(m):
        if A[i][j]==1:
            G.add_edge(rows[i],columns[j],weight=W[i][j])

def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

save_graph(G,"graph_first_pint")

###SECOND POINT
###PART A

#create list of id conference
conference=[]
for element in data:
    conference.append(element['id_conference_int'])
conference=set(conference)
conference=list(conference)
#print(conference)

#Create a dictionary with the conferences of each author
default_value = None
conf_author = dict.fromkeys(conference,default_value)
for a in conf_author.keys():
    for element in data:
        #for i in element['conference']:
        if (a==element['id_conference_int']):
            if (conf_author[a]==None):
                conf_author[a]=[element['authors'][0]['author_id']]
            else:
                conf_author[a].append(element['authors'][0]['author_id'])
#print(conf_author)

'''given a conference in input, return the subgraph induced by the set of 
authors who published at the input conference at least once.'''

input_conf=int(input())
res=[]
for k,v in conf_author.items():
    if k==input_conf:
        res=v
#print(res)

#Create the subgraph and plot
from matplotlib import pylab as pl
   
pos = nx.spring_layout(G)  #setting the positions with respect to G, not k.
k = G.subgraph(res)  

pl.figure()
nx.draw_networkx(k, pos=pos)

othersubgraph = G.subgraph(range(6,G.order()))
nx.draw_networkx(othersubgraph, pos=pos, node_color = 'b')
pl.show()


#Find betweenness, closeness and degree
betweenness = nx.betweenness_centrality(k)
closeness = nx.closeness_centrality(k)
degree = nx.degree(k)


#first plot


values=[]
for x in betweenness.keys():
    values.append(betweenness[x])
plt.hist(values)
plt.xlabel('Betweeness')
plt.ylabel('Frequency of nodes')
plt.title('Betweeness')
plt.show()


#second plot


values=[]
for x in closeness.keys():
    values.append(closeness[x])
plt.hist(values)
plt.xlabel('Closeness')
plt.ylabel('Frequency of nodes')
plt.title('Closeness')
plt.show()

#third plot
values=[]
for x in degree.keys():
    values.append(degree[x])
plt.hist(values)
plt.xlabel('Degree')
plt.ylabel('Frequency of nodes')
plt.title('Degree')
plt.xticks(range(min(degree.values()), max(degree.values())))
plt.show()

###PART B
nodos=G.nodes()
res=[]
input_authB=int(input())
d= int(input())
for i in c:
    if input_authB in i:
        res.append(i)
nres=[j for i in res for j in i]

from collections import Counter
count=Counter(nres)

del count[input_authB]
fres=[]
for k,v in count.items():
    if v<=d:
        fres.append(k)

from matplotlib import pylab as pl
   
pos = nx.spring_layout(G)  #setting the positions with respect to G, not k.
k = G.subgraph(fres)  

pl.figure()
nx.draw_networkx(k, pos=pos)

othersubgraph = G.subgraph(range(6,G.order()))
nx.draw_networkx(othersubgraph, pos=pos, node_color = 'b')
pl.show()


#####THIRD POINT
####PART A

import math
def DijkstraA(G,inicio,fin):

    path=[inicio]
    nodos=G.nodes()
    nodos=list(map(int, nodos))
    dist=[math.inf]*len(nodos)
    acum=0
    listAcum=[0]
    d=dict(zip(nodos,dist))
    actual=inicio
    if fin not in G.neighbors(inicio):
        while actual!=fin:
            for k in d.keys():
                if G.has_edge(actual,k)== True and k not in path:
                    if d[k]==math.inf:
                        d[k]=G[actual][k]['weight']
                    else:
                        if d[k]>acum+G[actual][k]['weight']:
                            d[k]=acum+G[actual][k]['weight']
                if k in path:
                    d[k]=math.inf
            actual=min(d.items(), key=lambda x: x[1])[0]

            if G.has_edge(actual,path[-1])==False:
                #print("path:",path)
                while G.has_edge(actual,path[-1])==False:
                    del path[-1]
                    acum=acum-listAcum[-1]
                    del listAcum[-1]
            #print(path)
            path.append(actual)
            acum=acum+d[actual]
            listAcum.append(d[actual])
            #print(path)
    else:
        d[fin]=G[inicio][fin]['weight']
        path.append(fin)
        acum=acum+d[fin]
        listAcum.append(d[fin])
    return path,acum

input_author=int(input())
id_aris=256176
try:
    print(DijkstraA(G,input_author,id_aris))
except IndexError:
    print("There is no path")
    
    
###PART B

total_nodes=G.nodes()
set_nodes=list(map(int,input().split()))

if len(set_nodes)>=21:
    print("Cardinality >= 21")
else:
    groupNumber={key: None for key in total_nodes}
    #print(groupNumber)
    for i in total_nodes:
        #print(i)
        db={}
        for j in set_nodes:
            NoError=True
            try:
                path,acum=DijkstraA(G,i,j)
                NoError=True
            except IndexError:
                NoError=False
            if NoError==True:
                db.update({path:acum})
        if NoError==True:
            minimoGN=min(db.items(),key=lambda x:x[1])[0]
        else:
            minimoGN="There is no path"
        groupNumber.update({i:minimoGN})
print(groupNumber)