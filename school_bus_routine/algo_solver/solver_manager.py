from .held_karp_solver import HeldKarpSolver
from .ant_colony_solver import AntColonySolver
from .greedy_solver import GreedySolver
from utils.file_manager import FileManager
from utils.matrix_generator import DynamicMatrixGenerator
import time


class SolverManager:

    def __init__(self, api_key, node_mapping, output_file_path):
        self.api_key = api_key
        self.node_mapping = node_mapping
        self.output_file_path = output_file_path
        self.results = []
        self.dm_generator = DynamicMatrixGenerator(self.api_key, self.node_mapping)
        self.distance_matrix = self.generate_distance_matrix()

    def generate_distance_matrix(self):
        self.dm_generator.generate_distance_matrix()
        self.dm_generator.add_all_distances()

        # write the matrix to the output file
        with open(self.output_file_path, "w") as file:
            file.write("Matrix from Google Maps API:\n")
            self.dm_generator.write_matrix(file=file)

        return self.dm_generator.matrix

    def run_solver(self, solver_class, **kwargs):
        start_time = time.time()
        solver = solver_class(self.distance_matrix, **kwargs)
        cost, path = solver.solve()
        running_time = time.time() - start_time
        return cost, path, running_time

    def adjust_path(self, paths):
        modified_paths = [node + 1 for node in paths]
        path_with_labels = ["N" + str(node) for node in modified_paths]
        return path_with_labels

    def compare_algo_solver(self):

        # Greedy Algorithm
        greedy_cost, greedy_path, greedy_time = self.run_solver(GreedySolver)
        self.results.append(
            ("Greedy", greedy_cost, self.adjust_path(greedy_path), greedy_time)
        )
        FileManager.write_algo_results(
            "Greedy",
            greedy_cost,
            self.adjust_path(greedy_path),
            greedy_time,
            self.output_file_path,
        )

        # Held-Karp Algorithm
        hk_cost, hk_path, hk_time = self.run_solver(HeldKarpSolver)
        self.results.append(("Held-Karp", hk_cost, self.adjust_path(hk_path), hk_time))
        FileManager.write_algo_results(
            "Held-Karp",
            hk_cost,
            self.adjust_path(hk_path),
            hk_time,
            self.output_file_path,
        )

        # Ant Colony Optimization
        aco_args = {
            "n_ants": 10,
            "n_iterations": 100,
            "decay": 0.5,
            "alpha": 1,
            "beta": 2,
        }
        aco_cost, aco_path, aco_time = self.run_solver(AntColonySolver, **aco_args)
        self.results.append(
            ("Ant Colony Optimization", aco_cost, self.adjust_path(aco_path), aco_time)
        )
        FileManager.write_algo_results(
            "Ant Colony Optimization",
            aco_cost,
            self.adjust_path(aco_path),
            aco_time,
            self.output_file_path,
        )

        # Find the fastest algorithm
        fastest_result = min(self.results, key=lambda x: x[3])
        FileManager.write_fastest_result(fastest_result, self.output_file_path)

        # Draw the fastest algorithm paths into images
        self.dm_generator.draw_route(fastest_result[2])

        return fastest_result
