import numpy as np

class MatrixGenerator:
    @staticmethod
    def generate_distance_matrix(n, seed=None):
        """
        生成一个n x n的随机距离矩阵。
        """
        if seed is not None:
            np.random.seed(seed)  # 设置随机种子
        matrix = np.random.randint(1, 100, size=(n, n))  # 生成随机整数矩阵
        np.fill_diagonal(matrix, 0)  # 将对角线元素设置为无穷大
        return matrix
