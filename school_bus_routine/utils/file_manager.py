class FileManager:

    @staticmethod
    def read_node_mapping(file_path):
        node_mapping = {}
        with open(file_path, "r") as file:
            for index, line in enumerate(file, start=1):
                # strip whitespace and newline characters from the line
                address = line.strip()
                if address:
                    # create the dictionary entry with the prefix "Node "
                    node_mapping[f"N{index}"] = address
        return node_mapping

    @staticmethod
    def write_algo_results(algorithm_name, cost, path, running_time, file_path):
        with open(file_path, "a") as file:  # 'a' mode for append to file
            file.write(
                f"\n{algorithm_name} Algorithm: \n"
                f"Cost = {cost}, Path = {path}, Running time = {running_time:.10f} seconds\n"
            )

    @staticmethod
    def write_fastest_result(fastest_result, file_path):
        with open(file_path, "a") as file:
            file.write("\nIdeal Algorithm:\n")
            file.write(f"Algorithm: {fastest_result[0]}\n")
            file.write(f"Cost: {fastest_result[1]}\n")
            file.write(f"Path: {fastest_result[2]}\n")
            file.write(f"Running Time: {fastest_result[3]} seconds\n")
