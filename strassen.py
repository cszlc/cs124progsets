import numpy as np
import math
import time
import sys

# Helper functions like generate_random_matrix, check_power_two, nextPowerOf2, padding_zeroes, etc., remain the same
def generate_random_matrix(n):
    # Generate an n x n matrix with random values between 1 and 10
    return np.random.randint(0, 2, size=(n, n))

def split_matrix(a):
    mid = a.shape[0] // 2
    return a[:mid, :mid], a[:mid, mid:], a[mid:, :mid], a[mid:, mid:]

def check_power_two(n):
    while (n % 2 == 0 and n > 1):
       n = n // 2
    return n == 1

def matrix_mult(matrix_a, matrix_b):
    n = matrix_a.shape[0]  # Use .shape[0] for consistency
    result = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i, j] += matrix_a[i, k] * matrix_b[k, j]
    return result

def nextPowerOf2(n):
    return int(2 ** (math.ceil(math.log(n, 2))))

def padding_zeroes(M):
    n = M.shape[0]
    M_padded_size = nextPowerOf2(n)
    # Ensure the padding is with integer zeroes
    pad_width = ((0, M_padded_size - n), (0, M_padded_size - n))
    return np.pad(M, pad_width, mode='constant', constant_values=0).astype(int)

def strassen(matrix_a, matrix_b):
    n = matrix_a.shape[0]
    if not check_power_two(n):
        matrix_a = padding_zeroes(matrix_a)
        matrix_b = padding_zeroes(matrix_b)
    
    if n <= 512:
        result = matrix_mult(matrix_a, matrix_b)
        return result[:n, :n]
    
    A, B, C, D = split_matrix(matrix_a)
    E, F, G, H = split_matrix(matrix_b)

    p1 = strassen(A, F - H)
    p2 = strassen(A + B, H)
    p3 = strassen(C + D, E)
    p4 = strassen(D, G - E)
    p5 = strassen(A + D, E + H)
    p6 = strassen(B - D, G + H)
    p7 = strassen(A - C, E + F)

    top_left = p5 + p4 - p2 + p6
    top_right = p1 + p2
    bot_left = p3 + p4
    bot_right = p1 + p5 - p3 - p7

    # Construct the result matrix from the quadrants
    new_matrix_top = np.hstack((top_left, top_right))
    new_matrix_bot = np.hstack((bot_left, bot_right))
    full_result = np.vstack((new_matrix_top, new_matrix_bot))

    # Return the top-left submatrix that corresponds to the original size
    return full_result[:n, :n].astype(int)

# Read input matrices from a file
def read_matrices(filename, n):
    with open(filename, 'r') as file:
        data = file.read().splitlines()
    data = [int(float(val.strip())) for val in data]
    matrix_a = np.array(data[:n**2]).reshape(n, n)
    matrix_b = np.array(data[n**2:]).reshape(n, n)
    return matrix_a, matrix_b

# Output the diagonal elements of the matrix
def output_diagonal(matrix):
    for i in range(matrix.shape[0]):
        print(int(matrix[i, i]))

def main(flag, dimension, inputfile):
    n = int(dimension)
    matrix_a, matrix_b = read_matrices(inputfile, n)
    result = strassen(matrix_a, matrix_b)
    output_diagonal(result)

if __name__ == "__main__":
    # The program is called with the flag, the dimension of the matrices, and the filename of the input
    if len(sys.argv) != 4:
        print("Usage: python strassen.py flag dimension inputfile")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])