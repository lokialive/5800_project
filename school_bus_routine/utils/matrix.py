import numpy as np
from .google_maps import GoogleMapsUtil
import itertools


class DynamicMatrixGenerator:

    def __init__(self, api_key, node_mapping):
        self.matrix = None
        self.node_mapping = node_mapping
        self.labels = list(node_mapping.keys())  # the keys from node_mapping are labels
        self.google_map = GoogleMapsUtil(api_key=api_key)

    def generate_distance_matrix(self):
        """Initialize an n x n distance matrix with zeros or arbitrary large values."""
        n = len(self.labels)
        self.matrix = np.full((n, n), np.inf)
        # Use np.inf to represent no direct connection
        np.fill_diagonal(self.matrix, 0)
        # Diagonal is zero because distance to self is zero
        self.labels = [f"Node {i+1}" for i in range(n)]

    def add_distance(self, node1, node2):
        """Add a distance between two nodes using the node mapping."""
        actual_node1 = self.node_mapping[node1]
        actual_node2 = self.node_mapping[node2]
        idx1 = self.labels.index(node1)
        idx2 = self.labels.index(node2)
        distance_mile = self.google_map.calculate_distance(actual_node1, actual_node2)
        self.matrix[idx1, idx2] = distance_mile
        self.matrix[idx2, idx1] = distance_mile  # Assuming undirected graph

    def add_all_distances(self):
        """Add distances between all pairs of nodes."""
        for node1, node2 in itertools.combinations(self.labels, 2):
            self.add_distance(node1, node2)

    def remove_connection(self, node1, node2):
        """Remove a connection by setting the distance to infinity (no direct path)."""
        idx1 = self.labels.index(node1)
        idx2 = self.labels.index(node2)
        self.matrix[idx1, idx2] = np.inf
        self.matrix[idx2, idx1] = np.inf  # Assuming undirected graph

    def update_label(self, old_label, new_label):
        """Update a node's label."""
        idx = self.labels.index(old_label)
        self.labels[idx] = new_label

    def print_matrix(self):
        """Print the current distance matrix with labels."""
        print("\t" + "\t".join(self.labels))
        for label, row in zip(self.labels, self.matrix):
            print(f"{label}\t" + "\t".join(map(str, row)))
