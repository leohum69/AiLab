import pandas as pd
import numpy as np
import random

# Function to read and preprocess the data
def load_and_preprocess_data(file_path):
    # Read data
    data = pd.read_csv(file_path)
    
    # Check for missing values
    print("Missing values in the dataset:")
    print(data.isnull().sum())
    
    # Handle categorical features (convert to numeric)
    categorical_columns = ['Education', 'WorkType', 'Gender', 'Region']
    for col in categorical_columns:
        if col in data.columns:
            data[col] = pd.factorize(data[col])[0]
    
    return data

# Implement K-means clustering algorithm
class KMeansClustering:
    def __init__(self, n_clusters=10, max_iter=100, random_state=None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids = None
        self.labels = None
    
    def fit(self, X):
        # Set random seed for reproducibility
        if self.random_state is not None:
            np.random.seed(self.random_state)
        
        # Initialize centroids randomly
        min_vals = X.min(axis=0)
        max_vals = X.max(axis=0)
        
        # Generate random centroids within the feature space
        self.centroids = np.array([np.random.uniform(min_vals, max_vals) for _ in range(self.n_clusters)])
        
        # Iterate until convergence or max_iter
        for _ in range(self.max_iter):
            # Assign each point to the nearest centroid
            self.labels = self._assign_clusters(X)
            
            # Store old centroids for convergence check
            old_centroids = self.centroids.copy()
            
            # Update centroids based on assigned points
            self._update_centroids(X)
            
            # Check for convergence
            if np.all(old_centroids == self.centroids):
                break
        
        return self
    
    def _assign_clusters(self, X):
        # Calculate distances to each centroid
        distances = np.zeros((X.shape[0], self.n_clusters))
        
        for i in range(self.n_clusters):
            # Euclidean distance between each data point and the centroid
            distances[:, i] = np.sqrt(np.sum((X - self.centroids[i])**2, axis=1))
        
        # Assign each point to the closest centroid
        return np.argmin(distances, axis=1)
    
    def _update_centroids(self, X):
        for i in range(self.n_clusters):
            # Get all points assigned to this cluster
            cluster_points = X[self.labels == i]
            
            # If no points are assigned to this cluster, don't update the centroid
            if len(cluster_points) > 0:
                self.centroids[i] = np.mean(cluster_points, axis=0)
    
    def predict(self, X):
        return self._assign_clusters(X)

# Main function to run the K-means algorithm
def main():
    # File path 
    file_path = "Dataset2.csv"
    
    # Load and preprocess the data
    data = load_and_preprocess_data(file_path)
    
    # Print basic info about the dataset
    print("\nDataset Information:")
    print(f"Number of samples: {data.shape[0]}")
    print(f"Number of features: {data.shape[1]}")
    print("\nFeatures:", data.columns.tolist())
    print("\nFirst few rows of the preprocessed data:")
    print(data.head())
    
    # Select numerical features for clustering
    features = data.select_dtypes(include=['int64', 'float64'])
    
    # Scale features (standardization)
    scaled_features = (features - features.mean()) / features.std()
    
    # Apply K-means clustering
    kmeans = KMeansClustering(n_clusters=10, max_iter=100, random_state=42)
    kmeans.fit(scaled_features.values)
    
    # Add cluster labels to the original data
    data['Cluster'] = kmeans.labels
    
    # Display the clusters
    print("\nNumber of data points in each cluster:")
    for i in range(10):
        cluster_data = data[data['Cluster'] == i]
        print(f"Cluster {i}: {len(cluster_data)} data points")
    
    # Display first few rows of each cluster
    for i in range(10):
        cluster_df = data[data['Cluster'] == i]
        print(f"\nCluster {i} (showing first 3 rows):")
        print(cluster_df.head(3))
    
    return data

if __name__ == "__main__":
    clustered_data = main()