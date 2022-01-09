from sklearn.cluster import AgglomerativeClustering
import numpy as np

def HierarchicalClusters(listofVectors):
    X = np.array(listofVectors)
    clustering = AgglomerativeClustering().fit(X)
    return clustering.labels_

if __name__ == '__main__':
    listofVectors = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]
    print(HierarchicalClusters(listofVectors))
    # X = np.array([[1, 2], [1, 4], [1, 0],
    #           [4, 2], [4, 4], [4, 0]])
    # clustering = AgglomerativeClustering().fit(X)
    # print(clustering.labels_)