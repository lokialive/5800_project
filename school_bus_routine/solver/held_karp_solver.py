from .tsp_solver import TSPSolver


"""
Concrete Implementation of TSPSolver -- applies Held-Karp Algorithm
"""


class HeldKarpSolver(TSPSolver):
    def solve(self):
        # dictionary used for memoization to store the minimum cost to reach each subset of points from each starting point
        memo = {}
        # use self.distance_matrix to access the distance matrix
        all_points_set = frozenset(range(1, len(self.distance_matrix)))

        def search(start, points_set):
            if points_set == frozenset():
                return self.distance_matrix[start][0], [
                    0
                ]  # Return to the starting point
            elif (start, points_set) in memo:
                return memo[(start, points_set)]
            else:
                min_cost = float("inf")
                min_path = []
                for endpoint in points_set:
                    remaining_points_set = points_set - frozenset([endpoint])
                    cost, path = search(endpoint, remaining_points_set)
                    current_cost = self.distance_matrix[start][endpoint] + cost
                    if current_cost < min_cost:
                        min_cost = current_cost
                        min_path = [endpoint] + path
                memo[(start, points_set)] = (min_cost, min_path)
                return min_cost, min_path

        # Start the search from the first point (assuming 0 is the starting point)
        min_cost, min_path = search(0, all_points_set)
        return min_cost, [0] + min_path
