import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

def kmeans(data, k):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(data)
    return (kmeans.cluster_centers_, kmeans.labels_)

if __name__ == '__main__':
    data = np.array([[1, 2], [1, 4], [1, 0],
                [10, 2], [10, 4], [10, 0]])
    k = 3
    kmeans(data, k)