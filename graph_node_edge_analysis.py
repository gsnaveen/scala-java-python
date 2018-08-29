import pandas as pd
import networkx as nx

databasedf = pd.read_csv("./data/inputData.txt",sep='\t',header=0 )

G= nx.DiGraph()
for index,row in databasedf.iterrows():
    G.add_edge(row["parent"],row["child"])
    
print("Number of Nodes: " + str(G.number_of_nodes())) # 5581
G.number_of_edges() # 90341
print("Avg of Edges: " + str(round(G.number_of_edges()/G.number_of_nodes(),2))) 
root = list(nx.topological_sort(G))[0] #Topological sort not defined on undirected graphs.
print("Root Key : "+root)

MaxVal = 0
for node in G.nodes():
    mydata = set()
    for ChildNode in G.edges(node):
        for grandChild in G.edges(ChildNode):
            mydata.add(grandChild)

    if len(mydata) > MaxVal:
        MaxVal = len(mydata)
        MaxNode = node
        
print("Node Max Grand Child : " + str(MaxNode) +", " + str(MaxVal)) 

#Check if there is a Cycle in a graph
#nx.find_cycle(G, orientation='original')
for i in list(nx.simple_cycles(G)):
    print(i)
	
#All descendants of the node
nodeHash = {'myNode':1}
nextLevel = ['myNode']
nextTONext = []

while nextLevel:
    nextTONext = set()
    for node in nextLevel:
        for parentNode, childnode in G.edges(node):
            #print(childnode)
            if childnode in nodeHash.keys():
                nodeHash[childnode] += 1
            else:
                nodeHash[childnode] = 1
                
            nextTONext.add(childnode)
        
    nextLevel = list(nextTONext)

#for scc in nx.strongly_connected_components(G):
for scc in nx.strongly_connected_component_subgraphs(G,copy=True):
    print(scc)

import matplotlib.pyplot as plt
# nx.draw_circular(G)
# nx.draw_spectral(G)
# nx.draw_random(G)
nx.draw(G)
plt.show()
plt.savefig("path.png")

### Input file has 2 fields Parent and Child
