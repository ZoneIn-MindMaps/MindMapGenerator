from sklearn.cluster import DBSCAN
import numpy as np

def DBSCANClusters(listofVectors):
    X = np.array(listofVectors)
    clustering = DBSCAN(eps=0.5, min_samples=10).fit(X)
    return clustering.labels_

if __name__ == '__main__':
    listofVectors = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]
    print(DBSCANClusters(listofVectors))