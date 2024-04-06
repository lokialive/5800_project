from abc import ABC, abstractmethod

class TSPSolver(ABC):
    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix

    @abstractmethod
    def solve(self):
        pass
