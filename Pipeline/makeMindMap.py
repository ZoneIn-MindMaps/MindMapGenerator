import matplotlib.pyplot as plt
import networkx as nx
import my_networkx as my_nx
from itertools import groupby

def makeGraph(labels, timestamps):
    n = len(labels)
    dic = {}
    res = [i[0] for i in groupby(labels)]
    for i in range(n):
        if labels[i] not in dic:
            dic[labels[i]] = [i]
        else:
            dic[labels[i]].append(i)
    Timestamp = []
    j = 0
    for i in range(1, len(labels)):
        if labels[j] == labels[i]:
            j+=1
        else:
            Timestamp.append(timestamps[j])
            j+=1
    From = res[0:-1]
    To = res[1:]
    temp = []
    i = 0
    for n1, n2 in zip(From, To):
        temp.append(((n1, n2, {'w':Timestamp[i]})))
        i+=1
    print(temp)
    size = 2000
    G = nx.DiGraph()
    edge_list = temp
    G.add_edges_from(edge_list)
    pos=nx.spring_layout(G,seed=5)
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=size)
    nx.draw_networkx_labels(G, pos, ax=ax)
    curved_edges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
    straight_edges = list(set(G.edges()) - set(curved_edges))
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=straight_edges, node_size=size)
    arc_rad = 0.25
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}', node_size=size)
    edge_weights = nx.get_edge_attributes(G,'w')
    curved_edge_labels = {edge: edge_weights[edge] for edge in curved_edges}
    straight_edge_labels = {edge: edge_weights[edge] for edge in straight_edges}
    my_nx.my_draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=curved_edge_labels,rotate=False,rad = arc_rad)
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=straight_edge_labels,rotate=False)
    fig.savefig("/home/zoners/ZoneIn-Organisation/zonein/public/images/mindmap.png", bbox_inches='tight', pad_inches=0, transparent=True)
    # toReturn = {}
    # print
    return tuple(temp)
if __name__ == "__main__":
    temp = makeGraph([3, 2, 3, 3, 0, 3, 0, 1, 1, 1, 1, 1, 3, 0, 1, 1, 1, 1, 1, 1, 1, 1,
        2, 2, 1, 2, 2, 3, 1, 3, 0, 3, 3, 3, 3, 2, 2, 2, 1, 3, 2, 2, 3, 2,
        1, 3, 2, 2, 1, 3, 0, 0, 0, 0, 0, 0, 0, 2, 3, 1, 2, 1, 0, 1, 1, 0,
        1, 0, 3, 0, 0, 3, 0, 2, 1, 1, 1, 0, 1, 0, 2, 3, 0, 0, 3, 3, 0, 0,
        2, 2, 3, 3, 1, 1, 1, 1, 1, 1, 2, 3, 1, 1, 2, 1, 0, 1, 1, 0, 2, 1,
        1, 3, 3, 2, 0, 3, 1, 2, 2, 2, 1, 1, 2, 1, 2, 0, 0, 0, 0, 1, 3, 0,
        1, 1, 3, 1, 0, 1, 3, 1, 0, 0, 0, 3, 0, 0, 0, 3, 2, 2, 0, 2, 2, 2,
        3, 0, 0, 3, 0, 0, 1, 2, 1, 0, 0, 0, 2, 0, 0, 0, 2, 2, 1, 2, 0, 1,
        2, 2, 2, 0, 3, 3, 3, 2, 2, 2, 2, 2, 0, 2, 2], [69.86999999999999, 91.89, 117.39, 145.742, 181.48, 228.52, 261.45000000000005, 289.99, 315.07, 343.87, 366.88, 393.55, 411.09999999999997, 434.965, 457.42, 487.81, 514.659, 536.62, 560.74, 583.15, 613.205, 638.83, 660.5899999999999, 687.22, 708.28, 730.21, 754.61, 777.4, 798.88, 827.17, 856.14, 879.27, 967.34, 995.15, 1039.069, 1070.44, 1097.98, 1125.4299999999998, 1151.95, 1179.01, 1199.99, 1216.27, 1239.85, 1263.1299999999999, 1286.24, 1304.8000000000002, 1332.85, 1353.07, 1381.76, 1431.93, 1455.72, 1481.97, 1509.51, 1531.74, 1554.84, 1580.22, 1603.68, 1628.91, 1648.77, 1672.83, 1701.618, 1726.8500000000001, 1745.1570000000002, 1767.0800000000002, 1792.48, 1815.53, 1843.83, 1870.68, 1897.08, 1918.8380000000002, 1942.32, 1967.21, 1995.03, 2021.1299999999999, 2046.18, 2071.32, 2091.65, 2114.79, 2133.88, 2172.93, 2196.39, 2215.33, 2243.985, 2267.34, 2286.24, 2318.713, 2346.54, 2370.06, 2393.1, 2416.71, 2437.9, 2465.8599999999997, 2491.59, 2525.32, 2547.8199999999997, 2568.73, 2591.3199999999997, 2612.41, 2636.1, 2669.34, 2694.6600000000003, 2724.15, 2752.54, 2777.41, 2803.01, 2825.9, 2843.948, 2870.33, 2894.2200000000003, 2920.2200000000003, 2946.7999999999997, 2969.53, 2993.33, 3015.35, 3043.04, 3071.48, 3099.49, 3124.7200000000003, 3146.173, 3168.26, 3195.1000000000004, 3214.9900000000002, 3231.85, 3250.7799999999997, 3270.05, 3294.16, 3322.36, 3354.73, 3378.1, 3404.634, 3437.253, 3461.29, 3489.4, 3510.0099999999998, 3536.177, 3561.5800000000004, 3583.06, 3610.33, 3632.87, 3655.12, 3676.42, 3698.26, 3716.53, 3744.46, 3773.6800000000003, 3795.3399999999997, 3815.1600000000003, 3843.51, 3869.6400000000003, 3897.42, 3918.48, 3944.88, 3964.47, 3987.75, 4007.88, 4046.35, 4075.315, 4089.6400000000003, 4111.742, 4133.986, 4156.675, 4176.12, 4200.63, 4225.7699999999995, 4251.990000000001, 4277.08, 4296.42, 4316.85, 4335.96, 4361.797, 4388.64, 4413.72, 4450.5, 4474.62, 4500.78, 4530.3, 4556.92, 4578.01, 4606.91, 4640.92, 4721.360000000001, 4782.293, 4806.349999999999, 4831.4, 4857.253, 4888.28, 4915.66, 4943.46, 4973.6, 4995.65, 5021.12])
    print(temp)
    print(type(temp))