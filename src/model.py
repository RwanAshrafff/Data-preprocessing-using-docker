#!/usr/bin/env python
# coding: utf-8

import sys
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

if __name__ == '__main__':
    # Check if the file path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python model.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]

    # Read the data
    df = pd.read_csv(file_path)

    # Select only numeric features for clustering
    numeric_features = df.select_dtypes(include=[np.number])
    if numeric_features.empty:
        print("No numeric features found for clustering.")
        sys.exit(1)

    # Apply K-means with k=3
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(numeric_features)

    # Save the number of records in each cluster
    cluster_counts = df['Cluster'].value_counts().sort_index()
    with open("service-result/k.txt", "w") as f:
        f.write("Cluster Sizes:\n")
        for cluster, count in cluster_counts.items():
            f.write(f"Cluster {cluster}: {count}\n")

    print("K-means clustering complete. Cluster sizes saved to 'service-result/k.txt'.")
