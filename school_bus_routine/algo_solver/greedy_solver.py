from .tsp_solver import TSPSolver
import numpy as np


class GreedySolver(TSPSolver):
    def solve(self):
        start = 0
        path = [start]
        total_cost = 0
        visited = set(path)
        n = len(self.distance_matrix)

        while len(path) < n:
            last = path[-1]
            next_city = None
            min_dist = np.inf
            for j in range(n):
                if j not in visited and self.distance_matrix[last][j] < min_dist:
                    next_city = j
                    min_dist = self.distance_matrix[last][j]
            path.append(next_city)
            visited.add(next_city)
            total_cost += min_dist

        # Add the distance from the last city back to the start
        total_cost += self.distance_matrix[path[-1]][start]
        path.append(start)  # Complete the circuit

        return total_cost, path
