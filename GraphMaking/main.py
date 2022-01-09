import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.layout import spring_layout
import pandas as pd

def makeGraph(labels, timestamps):
    n = len(labels)
    dic = {}
    for i in range(n):
        if labels[i] not in dic:
            dic[labels[i]] = [i]
        else:
            dic[labels[i]].append(i)
    g = nx.Graph()
    x = sorted(set(labels))
    node_sizes = [500]
    for i in labels:
        g.add_node(i)
    for i in range(len(x)-1):
        for j in range(len(dic[i])-1):
            g.add_edge(dic[i][j], dic[i][j+1])
            node_sizes.append(500+1000*i)
        g.add_edge(dic[i][0], dic[i+1][0])
        node_sizes.append(500+1000*(i+1))
    for j in range(len(dic[i])-1):
        g.add_edge(dic[len(x)-1][j], dic[len(x)-1][j+1])
        node_sizes.append(500+1000*(i+1))
    
    temp = []
    for n1, n2 in g.edges:
        temp.append(((n1, n2), timestamps[n2-1]))
    edge_labels = dict(temp)
    print(g.edges, g.number_of_nodes(), len(node_sizes))
    print(node_sizes)
    
    nx.draw_shell(g, with_labels=True, edgecolors='black', node_color='grey', node_size = node_sizes)
    nx.draw_networkx_edge_labels(g, nx.shell_layout(g), edge_labels = edge_labels)
    plt.savefig("resources/mindmap.png")

makeGraph([0, 0, 0, 0, 0, 1, 1, 0, 2, 2, 0, 0, 0], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.5, 8.0, 9.6, 10.0, 12.0, 15.0, 15.5])