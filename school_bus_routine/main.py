import time
from utils import MatrixGenerator
from solver.held_karp_solver import HeldKarpSolver
from solver.ant_colony_solver import AntColonySolver
from solver.greedy_solver import GreedySolver


def compare_solvers(n_points, n_matrices=5):
    for i in range(n_matrices):
        print(f"\nMatrix {i+1}:")
        distance_matrix = MatrixGenerator.generate_distance_matrix(n_points, seed=i)

        # 贪心算法
        start_time = time.time()
        greedy_solver = GreedySolver(distance_matrix)
        greedy_cost, greedy_path = greedy_solver.solve()
        greedy_time = time.time() - start_time
        print(f"Greedy Algorithm: Cost = {greedy_cost}, Path = {greedy_path}, Running time = {greedy_time} seconds")

        # Held-Karp 算法
        start_time = time.time()
        hk_solver = HeldKarpSolver(distance_matrix)
        hk_cost, hk_path = hk_solver.solve()
        hk_time = time.time() - start_time
        print(f"Held-Karp Algorithm: Cost = {hk_cost}, Path = {hk_path}, Running time = {hk_time} seconds")

        # 蚁群算法
        start_time = time.time()
        aco_solver = AntColonySolver(distance_matrix, n_ants=10, n_iterations=100, decay=0.5, alpha=1, beta=2)
        aco_cost, aco_path = aco_solver.solve()
        aco_time = time.time() - start_time
        print(f"Ant Colony Optimization: Cost = {aco_cost}, Path = {aco_path}, Running time = {aco_time} seconds")

def main():
    compare_solvers(n_points=10)

if __name__ == "__main__":
    main()
