import sys
from algo_solver.solver_manager import SolverManager
from utils.file_manager import FileManager
from utils.address_generator import AddressGenerator
from dotenv import load_dotenv
import os
import random

def main():
    # set up
    load_dotenv()
    center_address = "Snell Library, 360 Huntington Ave, Boston, MA 02115"
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    random_count = random.randint(2, 10)

    # generator 10 random locations
    address_generator = AddressGenerator(api_key)
    lat, lng = address_generator.get_location(center_address)
    random_points = address_generator.generate_random_points(lat, lng, 3.22, random_count)  # 2mile equals 3.22 km
    addresses = [address_generator.get_address(lat, lng) for lat, lng in random_points]
    with open("random_addresses.txt", "w") as file:
        for address in addresses:
            file.write(address + "\n")
    print("Addresses have been written to random_addresses.txt")

    address_file_path = "random_addresses.txt"
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
