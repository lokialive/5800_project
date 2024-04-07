import numpy as np
from .google_maps import GoogleMapsUtil
import itertools


class DynamicMatrixGenerator:

    def __init__(self, api_key, node_mapping):
        self.matrix = None
        self.node_mapping = node_mapping
        self.labels = list(node_mapping.keys())  # the keys from node_mapping are labels
        self.google_map = GoogleMapsUtil(api_key=api_key)
        self.location_strings = (
            {}
        )  # dict to store the latitude and longitude of the location in the node_mapping

    def generate_distance_matrix(self):
        """Initialize an n x n distance matrix with zeros or arbitrary large values."""
        n = len(self.labels)
        self.matrix = np.full((n, n), np.inf)
        # Use np.inf to represent no direct connection
        np.fill_diagonal(self.matrix, 0)
        # Diagonal is zero because distance to self is zero
        self.labels = [f"N{i+1}" for i in range(n)]

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

    def draw_route(self, path=None):
        # get coordinate of each location in the node_mapping and save it to location_string
        for key, value in self.node_mapping.items():
            self.location_strings[key] = self.google_map.get_coordinates(value)
        # draw the route based on the locations
        # print(self.location_strings)
        self.google_map.plot_nodes(self.location_strings, self.node_mapping, path)

    def remove_connection(self, node1, node2):
        """Remove a connection by setting the distance to infinity (no direct path)."""
        idx1 = self.labels.index(node1)
        idx2 = self.labels.index(node2)
        self.matrix[idx1, idx2] = np.inf
        self.matrix[idx2, idx1] = np.inf

    def update_label(self, old_label, new_label):
        """Update a node's label."""
        idx = self.labels.index(old_label)
        self.labels[idx] = new_label

    def write_matrix(self, file):
        max_label_length = max(len(label) for label in self.labels)
        output = (
            "\t"
            + "\t".join(f" {label:>{max_label_length}}" for label in self.labels)
            + "\n"
        )
        for label, row in zip(self.labels, self.matrix):
            formatted_row = " \t".join(
                f"{value:>{max_label_length}.2f}" if not np.isinf(value) else "inf"
                for value in row
            )
            output += f"{label:>{max_label_length}}\t{formatted_row}\n"

        file.write(output)
