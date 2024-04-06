import numpy as np
from .tsp_solver import TSPSolver


class TSPProblem:
    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix
        self.size = len(distance_matrix)


class AntColonySolver(TSPSolver):
    def __init__(
        self, distance_matrix, n_ants=10, n_iterations=100, decay=0.5, alpha=1, beta=2
    ):
        super().__init__(distance_matrix)  # Call the base class constructor
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.pheromone = np.ones(self.distance_matrix.shape) / len(self.distance_matrix)

    def solve(self):
        best_cost = float("inf")
        best_path = None
        for _ in range(self.n_iterations):
            paths = [self.generate_path(0) for _ in range(self.n_ants)]
            self.update_pheromone(paths)
            for path, cost in paths:
                if cost < best_cost:
                    best_cost = cost
                    best_path = path
        return best_cost, best_path

    def generate_path(self, start):
        path = [start]
        n = len(self.distance_matrix)
        visited = set([start])

        while len(path) < n:
            current = path[-1]
            move_probabilities = self.move_probabilities(current, visited)
            next_city = self.roulette_wheel_selection(move_probabilities)
            if next_city is not None:
                path.append(next_city)
                visited.add(next_city)
            else:
                break

        path.append(start)  # Complete the tour
        cost = self.path_cost(path)
        return path, cost

    def move_probabilities(self, current, visited):
        pheromones = np.copy(self.pheromone[current])
        distances = np.array(self.distance_matrix[current][:], dtype=float)
        distances[distances == 0] = 1e-10

        for i in visited:
            pheromones[i] = 0

        desirability = np.power(pheromones, self.alpha) * np.power(
            1.0 / distances, self.beta
        )

        if np.sum(desirability) == 0:
            return np.zeros(len(distances))
        else:
            probabilities = desirability / np.sum(desirability)
            return probabilities

    def roulette_wheel_selection(self, probabilities):
        cumulative_probabilities = np.cumsum(probabilities)
        r = np.random.rand()
        for i, cumulative_probability in enumerate(cumulative_probabilities):
            if r <= cumulative_probability:
                return i
        return len(probabilities) - 1

    def path_cost(self, path):
        return sum(
            [self.distance_matrix[path[i], path[i + 1]] for i in range(len(path) - 1)]
        )  # Use self.distance_matrix directly

    def update_pheromone(self, paths):
        self.pheromone *= 1 - self.decay
        for path, cost in paths:
            for i in range(len(path) - 1):
                self.pheromone[path[i]][path[i + 1]] += 1.0 / cost
