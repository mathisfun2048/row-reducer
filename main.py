
def get_matrix():
    print("Enter The following numbers: ")
    num_rows = int(input("number of rows: "))
    num_cols = int(input("number of cols: "))
    matrix = []

    print("enter row by row, space seperated:")
    for _ in range(num_rows):
        r = list(map(float, input(f"Row {_+1}: ").split()))
        if len(r) != num_cols:
            raise ValueError(f"inccorect number of values, each row needs to have {num_cols} numbers")
        matrix.append(r)
        
    return matrix

def get_vector():
    print("Enter the values in the vector")
    v = list(map(float, input(f"Vector: ").split()))
    return v

def rref(matrix):
    A = [row[:] for row in matrix]
    num_rows = len(A)
    num_cols = len(A[0])

    current_row = 0

    for c in range(num_cols):
        pivot_row = None
        for r in range(current_row, num_rows):
            if abs(A[r][c]) > 1e-10:
                pivot_row = r
                break
        
        if pivot_row is None:
            continue

        A[current_row], A[pivot_row] = A[pivot_row], A[current_row]

        pivot = A[current_row][c]
        A[current_row] = [x / pivot for x in A[current_row]]

        for r in range(num_rows):
            if r != current_row:
                factor = A[r][c]
                A[r] = [A[r][i] - factor * A[current_row][i] for i in range(num_cols)]

        current_row += 1
        if current_row >= num_rows:
            break

    return A

def lu(matrix):
    A = [row[:] for row in matrix]
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    if num_rows != num_cols:
        raise ValueError("matrix must be square")
    
    L = [[0.0] * num_cols for _ in range (num_rows)]
    U = [[0.0] * num_cols for _ in range(num_rows) ]

    for i in range(num_rows):

        for j in range(i, num_rows):
        
            sum_val = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - sum_val

        for j in range(i, num_rows):
            if i == j:
                L[i][j] = 1.0
            else:
                sum_val = sum(L[j][k] * U[k][i] for k in range(i))
                L[j][i] = (A[j][i] - sum_val) / U[i][i]

    return L, U

# takes in 2 vectors as col vectors
def dot_product(v1, v2):
    return sum(a*b for a, b in zip(v1, v2))

# takes in 1 vector as a row vector
def magnitude(v):
    return sum(x**2 for x in v) ** 0.5

def qr(matrix):
    A = [row[:] for row in matrix]
    num_rows = len(A)
    num_cols = len(A[0])
    
    A_T = [[A[i][j] for i in range(num_rows)] for j in range(num_cols)]
    Q_T = []
    R = [[0.0] * num_cols for _ in range(num_cols)]

    for i in range(num_cols):
        v = A_T[i][:]
        for j in range(i):
            R[j][i] = dot_product(Q_T[j], A_T[i])
            v = [v[k] - R[j][i] * Q_T[j][k] for k in range(num_rows)]

        R[i][i] = magnitude(v)

        if abs(R[i][i]) < 1e-10:
            raise ValueError("Matrix is rank deficient")

        Q_T.append([v[k] / R[i][i] for k in range(num_rows)])

    Q = [[Q_T[i][j] for i in range(num_cols)] for j in range(num_rows)]
    
    return Q, R

def inverse(matrix):
    A = [row[:] for row in matrix]
    num_rows = len(A)

    augment = [matrix[i][:] + [1 if i == j else 0 for j in range(num_rows)] for i in range(num_rows)]

    for i in range(num_rows):
        pivot = augment[i][i]
        if abs(pivot) < 1e-10:
            raise ValueError("matrix is signular")
        
        for j in range(2 * num_rows):
            augment[i][j] /= pivot
        
        for k in range(num_rows):
            if k != i:
                factor = augment[k][i]
                for j in range (2 * num_rows):
                    augment[k][j] -= factor * augment [i][j]
    
    return [[augment[i][j] for j in range(num_rows, 2 * num_rows)] for i in range(num_rows)]

def det(matrix):
    A = [row[:] for row in matrix]
    num_rows = len(A)

    det = 1.0

    for i in range(num_rows):
        if abs(A[i][i]) < 1e-10:
            return 0.0
        
        for j in range(i + 1, num_rows):
            factor = A[j][i] / A[i][i]
            for k in range(i, num_rows):
                A[j][k] -= factor * A[i][k]
        
        det *= A[i][i]

    return det

def matrix_times_vector(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]

def matrix_mult(A, B):
    num_rows_A = len(A)
    num_cols_A = len(A[0])
    num_rows_B = len(B)
    num_cols_B = len(B[0])

    if(num_cols_A != num_rows_B):
        raise ValueError("matricies not multiplicable")
    
    product = [[0.0]* num_cols_B for _ in range(num_rows_A)]

    for i in range(num_rows_A):
        for j in range(num_cols_B):
            product[i][j] = sum(A[i][k] * B[k][j] for k in range(num_cols_A))

    return product

def solve_system(A, b):
    num_rows = len(A)

    L, U = lu(A)

    y = [0.0] * num_rows
    for i in range(num_rows):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
    
    x = [0.0] * num_rows
    for i in range(num_rows - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i+1, num_rows))) / U[i][i]

    return x

"""
def find_eigenvector(matrix, eigenvalue, tol=1e-10):
    num_rows = len(matrix)
    
    # Form (A - λI)
    A = [row[:] for row in matrix]
    for i in range(num_rows):
        A[i][i] -= eigenvalue
    
    # Use your existing rref function
    A = rref(A)
    
    # Find free variable (first column without leading 1)
    pivot_cols = []
    for i in range(num_rows):
        for j in range(num_rows):
            if abs(A[i][j]) > tol:
                pivot_cols.append(j)
                break
    
    free_var = next((j for j in range(num_rows) if j not in pivot_cols), num_rows - 1)
    
    # Build eigenvector
    v = [0.0] * num_rows
    v[free_var] = 1.0
    
    # Back-substitute (now works because RREF has zeros above pivots)
    for i in range(len(pivot_cols) - 1, -1, -1):
        col = pivot_cols[i]
        v[col] = -sum(A[i][j] * v[j] for j in range(col + 1, num_rows))
    
    norm = magnitude(v)
    return [x / norm for x in v] if norm > tol else v

def qr_algorithm(matrix, max_iter = 1000, tol = 1e-10):
    A = [row[:] for row in matrix]
    num_rows = len(A)

    for _ in range(max_iter):
        Q, R = qr(A)
        A_new = matrix_mult(R, Q)

        converged = True
        for i in range(num_rows):
            for j in range(num_rows):
                if i != j and abs(A_new[i][j]) > tol:
                    converged = False
        
        if converged:
            break
        A = A_new

    return [A[i][i] for i in range(num_rows)]

def diagonalize(matrix):

    A = [row[:] for row in matrix]
    num_rows = len(A)

    eigenvalues = qr_algorithm(A)

    eigenvectors = []

    for lam in eigenvalues:
        v = find_eigenvector(A, lam)
        eigenvectors.append(v)
    
    P = [[eigenvectors[j][i] for j in range(num_rows)] for i in range(num_rows)]

    if abs(det(P)) < 1e-10:
        raise ValueError("matrix not diagonalizable :p")
    
    D = [[0.0] * num_rows for _ in range(num_rows)]
    for i in range(num_rows):
        D[i][i] = eigenvalues[i]
    
    P_inv = inverse(P)

    return P, D, P_inv
"""


def rref_printer():
    matrix = get_matrix()
    result = rref(matrix)

    print("rref: ")
    for row in result:
        print([round(x, 6) for x in row])

def lu_printer():
    matrix = get_matrix()
    L, U = lu(matrix)

    print("L: ")
    for row in L:
        print([round(x, 6) for x in row])

    print("U: ")
    for row in U:
        print([round(x, 6) for x in row])

def qr_printer():
    matrix = get_matrix()
    Q, R = qr(matrix)

    print("Q: ")
    for row in Q:
        print([round(x, 6) for x in row])

    print("R: ")
    for row in R:
        print([round(x, 6) for x in row])

def dot_product_printer():
    
    print("You will enter 2 vectors")
    print("vector 1")
    v1 = get_vector()
    print("vector 2")
    v2 = get_vector()

    product = dot_product(v1, v2)

    
    
    

    print(f"the dot product of {v1} and {v2} is {product}")

def magnitude_printer():

    v = get_vector()

    print(f"the magnitude of {v} is {magnitude(v)}")

def inverse_printer():
    matrix = get_matrix()

    inv = inverse(matrix)

    for row in inv:
        print([round(x, 6) for x in row])

def det_printer():
    matrix = get_matrix()

    determinant = det(matrix)

    print(f"the determinant is {determinant}")

def matrix_times_vector_printer():
    v = get_vector()
    print(v)
"""
def diagonal_printer():
    matrix = get_matrix()
    P, D, P_inv = diagonalize(matrix)

    print("P: ")
    for row in P:
        print([round(x, 6) for x in row])

    print("D: ")
    for row in D:
        print([round(x, 6) for x in row])

    print("P_inv: ")
    for row in P_inv:
        print([round(x, 6) for x in row])

    

    print("/n")
    print("/n")

    test = matrix_mult( matrix_mult(P, D), P_inv)
    for row in test:
        print([round(x, 6) for x in row])
"""


if __name__ == "__main__":
   magnitude_printer()