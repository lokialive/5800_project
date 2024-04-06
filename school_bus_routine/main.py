import sys
from algo_solver.solver_manager import SolverManager
from utils.file_manager import FileManager
from dotenv import load_dotenv
import os


def main():
    # set up
    load_dotenv()
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    address_file_path = "addresses.txt"
    # get node mapping
    node_mapping = FileManager.read_node_mapping(address_file_path)

    # define output file path
    cwd = os.getcwd()
    PATH_CURRENT_FILE = os.path.abspath(cwd)
    PATH_RESULT = os.path.join(PATH_CURRENT_FILE, "result.txt")

    # compare the TSP algos,  write to files, and generate output route
    algo_solver = SolverManager(
        api_key, node_mapping=node_mapping, output_file_path=PATH_RESULT
    )
    algo_solver.compare_algo_solver()
    print("Result written done")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
