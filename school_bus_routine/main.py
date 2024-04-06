import time
import sys

# from school_bus_routine.utils.utils import MatrixGenerator
from solver.held_karp_solver import HeldKarpSolver
from solver.ant_colony_solver import AntColonySolver
from solver.greedy_solver import GreedySolver
from utils.matrix import DynamicMatrixGenerator
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY")


def run_solver(solver_class, distance_matrix, **kwargs):
    start_time = time.time()
    solver = solver_class(distance_matrix, **kwargs)
    cost, path = solver.solve()
    running_time = time.time() - start_time
    return cost, path, running_time


def print_results(algorithm_name, cost, path, running_time):
    # adjust the path to start from 1 instead of 0
    adjusted_path = [node + 1 for node in path]

    print(
        f"\n{algorithm_name} Algorithm: \nCost = {cost}, Path = {adjusted_path}, Running time = {running_time:.10f} seconds"
    )
    sys.stdout.flush()  # flush the output buffer to ensure the print statement is displayed immediately.


def compare_solvers(node_mapping):
    print("\nMatrix from Google Maps API:")
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    dm_generator = DynamicMatrixGenerator(api_key, node_mapping)

    # Generate the distance matrix based on node_mapping
    dm_generator.generate_distance_matrix()
    dm_generator.add_all_distances()
    dm_generator.print_matrix()
    distance_matrix = dm_generator.matrix

    # Greedy Algorithm
    greedy_cost, greedy_path, greedy_time = run_solver(GreedySolver, distance_matrix)
    print_results("Greedy", greedy_cost, greedy_path, greedy_time)

    # Held-Karp Algorithm
    hk_cost, hk_path, hk_time = run_solver(HeldKarpSolver, distance_matrix)
    print_results("Held-Karp", hk_cost, hk_path, hk_time)

    # Ant Colony Optimization
    aco_args = {
        "n_ants": 10,
        "n_iterations": 100,
        "decay": 0.5,
        "alpha": 1,
        "beta": 2,
    }
    aco_cost, aco_path, aco_time = run_solver(
        AntColonySolver, distance_matrix, **aco_args
    )
    print_results("Ant Colony Optimization", aco_cost, aco_path, aco_time)


def main(node_mapping):
    compare_solvers(node_mapping=node_mapping)


if __name__ == "__main__":
    node_mapping = {
        "Node 1": "Snell Library, 360 Huntington Ave, Boston, MA 02115",
        "Node 2": "Westland Avenue Apartments, 66 Westland Ave # 205, Boston, MA 02115",
        "Node 3": "Madison Park Apartments, 757 Shawmut Ave, Roxbury, MA 02119",
        "Node 4": "Douglass Park Apartments, 650 Columbus Ave, Boston, MA 02118",
    }
    try:
        main(node_mapping=node_mapping)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
