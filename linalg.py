#Input Validation Helpers

def validate_matrix(matrix, name="matrix"):
    
    if not matrix:
        raise ValueError(f"Invalid input: {name} cannot be empty")
    if not isinstance(matrix, list):
        raise ValueError(f"Invalid input: {name} must be a list")
    if not matrix[0]:
        raise ValueError(f"Invalid input: {name} cannot have empty rows")

    num_cols = len(matrix[0])
    for i, row in enumerate(matrix):
        if not isinstance(row, list):
            raise ValueError(f"Invalid input: {name} row {i} must be a list")
        if len(row) != num_cols:
            raise ValueError(f"Invalid input: {name} must have consistent row lengths")

    return len(matrix), num_cols

def validate_square_matrix(matrix, name="matrix"):
    
    num_rows, num_cols = validate_matrix(matrix, name)
    if num_rows != num_cols:
        raise ValueError(f"Invalid input: {name} must be square")
    return num_rows

def validate_vector(vector, name="vector"):
    
    if not vector:
        raise ValueError(f"Invalid input: {name} cannot be empty")
    if not isinstance(vector, list):
        raise ValueError(f"Invalid input: {name} must be a list")
    return len(vector)

# functions

def get_matrix():
    print("Enter The following numbers: ")
    num_rows = int(input("number of rows: "))
    num_cols = int(input("number of cols: "))
    matrix = []

    print("enter row by row, space seperated:")
    for _ in range(num_rows):
        r = list(map(float, input(f"Row {_+1}: ").split()))
        if len(r) != num_cols:
            raise ValueError(f"incorrect number of values, each row needs to have {num_cols} numbers")
        matrix.append(r)

    return matrix

def get_vector():
    print("Enter the values in the vector")
    v = list(map(float, input(f"Vector: ").split()))
    return v

def rref(matrix):
    num_rows, num_cols = validate_matrix(matrix)
    A = [row[:] for row in matrix]

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
    num_rows = validate_square_matrix(matrix)
    A = [row[:] for row in matrix]
    num_cols = num_rows

    L = [[0.0] * num_cols for _ in range (num_rows)]
    U = [[0.0] * num_cols for _ in range(num_rows) ]

    for i in range(num_rows):

        for j in range(i, num_rows):

            sum_val = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - sum_val

        if abs(U[i][i]) < 1e-10:
            raise ValueError("Matrix requires pivoting for LU decomposition (zero pivot encountered)")

        for j in range(i, num_rows):
            if i == j:
                L[i][j] = 1.0
            else:
                sum_val = sum(L[j][k] * U[k][i] for k in range(i))
                L[j][i] = (A[j][i] - sum_val) / U[i][i]

    return L, U

def dot_product(v1, v2):
    len1 = validate_vector(v1, "vector 1")
    len2 = validate_vector(v2, "vector 2")
    if len1 != len2:
        raise ValueError(f"Invalid input: vectors must have same length (got {len1} and {len2})")
    return sum(a*b for a, b in zip(v1, v2))

def magnitude(v):
    validate_vector(v)
    return sum(x**2 for x in v) ** 0.5

def qr(matrix):
    num_rows, num_cols = validate_matrix(matrix)
    A = [row[:] for row in matrix]
    
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
    num_rows = validate_square_matrix(matrix)

    augment = [matrix[i][:] + [1 if i == j else 0 for j in range(num_rows)] for i in range(num_rows)]

    for i in range(num_rows):
        pivot_row = i
        for k in range(i + 1, num_rows):
            if abs(augment[k][i]) > abs(augment[pivot_row][i]):
                pivot_row = k

        if pivot_row != i:
            augment[i], augment[pivot_row] = augment[pivot_row], augment[i]

        pivot = augment[i][i]
        if abs(pivot) < 1e-10:
            raise ValueError("matrix is singular")

        for j in range(2 * num_rows):
            augment[i][j] /= pivot

        for k in range(num_rows):
            if k != i:
                factor = augment[k][i]
                for j in range (2 * num_rows):
                    augment[k][j] -= factor * augment [i][j]

    return [[augment[i][j] for j in range(num_rows, 2 * num_rows)] for i in range(num_rows)]

def det(matrix):
    num_rows = validate_square_matrix(matrix)
    A = [row[:] for row in matrix]

    det = 1.0

    for i in range(num_rows):
        pivot_row = i
        for k in range(i + 1, num_rows):
            if abs(A[k][i]) > abs(A[pivot_row][i]):
                pivot_row = k

        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            det *= -1

        if abs(A[i][i]) < 1e-10:
            return 0.0

        for j in range(i + 1, num_rows):
            factor = A[j][i] / A[i][i]
            for k in range(i, num_rows):
                A[j][k] -= factor * A[i][k]

        det *= A[i][i]

    return det

def matrix_times_vector(A, v):
    num_rows, num_cols = validate_matrix(A, "matrix")
    vec_len = validate_vector(v, "vector")
    if num_cols != vec_len:
        raise ValueError(f"Invalid input: matrix columns ({num_cols}) must match vector length ({vec_len})")

    product = []
    for _ in range(num_rows):
        product.append(dot_product(A[_], v))

    return product

def matrix_mult(A, B):
    num_rows_A, num_cols_A = validate_matrix(A, "matrix A")
    num_rows_B, num_cols_B = validate_matrix(B, "matrix B")

    if num_cols_A != num_rows_B:
        raise ValueError(f"Invalid input: matrices not multiplicable (A columns: {num_cols_A}, B rows: {num_rows_B})")
    
    product = [[0.0]* num_cols_B for _ in range(num_rows_A)]

    for i in range(num_rows_A):
        for j in range(num_cols_B):
            product[i][j] = sum(A[i][k] * B[k][j] for k in range(num_cols_A))

    return product

def solve_system(A, b):
    num_rows = validate_square_matrix(A, "matrix")
    vec_len = validate_vector(b, "vector")
    if num_rows != vec_len:
        raise ValueError(f"Invalid input: matrix size ({num_rows}x{num_rows}) must match vector length ({vec_len})")

    A_inv = inverse(A)

    x = matrix_times_vector(A_inv, b)

    return x

    """
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
    
def transpose(matrix):
    num_rows, num_cols = validate_matrix(matrix)
    A = [row[:] for row in matrix]

    trans = [[0.0] * num_rows for _ in range(num_cols)]

    for i in range(num_rows):
        for j in range(num_cols):
            trans[j][i] = A[i][j]

    return trans

def trace(matrix):
    num_rows = validate_square_matrix(matrix)
    A = [row[:] for row in matrix]

    total = 0
    for i in range(num_rows):
        total += A[i][i]

    return total
        
def rank(matrix):
    validate_matrix(matrix)
    A = [row[:] for row in matrix]
    A1 = rref(A)

    r = 0
    for row in A1:
        if any(abs(x) > 1e-10 for x in row):
            r += 1
    return r
    
def null(matrix):
    _, num_cols = validate_matrix(matrix)
    r = rank(matrix)

    nul = num_cols - r

    return nul

def cross(v1, v2):
    len1 = validate_vector(v1, "vector 1")
    len2 = validate_vector(v2, "vector 2")

    if len1 != 3 or len2 != 3:
        raise ValueError(f"Invalid input: vectors must be 3-dimensional (got {len1} and {len2})")
    

    m1 = [[v1[0], v1[1]], [v2[0], v2[1]]]
    m2 = [[v1[0], v1[2]], [v2[0], v2[2]]]
    m3 = [[v1[1], v1[2]], [v2[1], v2[2]]]

    c = [det(m3), -det(m2), det(m1)]

    return c

def projection(a, v):
    validate_vector(a, "vector a")
    validate_vector(v, "vector v")

    v_dot_v = dot_product(v, v)
    if abs(v_dot_v) < 1e-10:
        raise ValueError("Invalid input: cannot project onto zero vector")

    scale = dot_product(a, v) / v_dot_v
    proj = [num * scale for num in v]

    return proj

def lin_ind(matrix):
    _, num_cols = validate_matrix(matrix)
    r = rank(matrix)

    return r == num_cols

def eigenvalues(matrix, max_iter = 1000, tol = 1e-10):
    validate_square_matrix(matrix)
    A = [row[:] for row in matrix]

    for _ in range(max_iter):
        Q, R = qr(A)
        A1 = matrix_mult(R, Q)

        converged = all(abs(A1[i][i] - A[i][i]) < tol for i in range(len(A)))

        if converged:
            return [A1[i][i] for i in range(len(A))]
        
        A = A1

    return [A[i][i] for i in range(len(A))]

def null_space(matrix):
    _, num_cols = validate_matrix(matrix)
    A = rref(matrix)

    pivot_cols = []
    for row in A:
        for j in range(num_cols):
            if abs(row[j]) > 1e-10:
                pivot_cols.append(j)
                break
    # print("Pivot cols:", pivot_cols)
    free_cols = [j for j in range(num_cols) if j not in pivot_cols]
    # print("Free cols:", free_cols)
    if not free_cols:
        return [[0.0] * num_cols]

    basis = []
    for free_col in free_cols:
        v = [0.0] * num_cols
        v[free_col] = 1.0

        for i, pivot_col in enumerate(pivot_cols):
            v[pivot_col] = -A[i][free_col]

        basis.append(v)

    return basis if basis else [[0.0] * num_cols]

def eigenvector(matrix, eigenvalue):
    num_rows = validate_square_matrix(matrix)
    A_shifted = [row[:] for row in matrix]

    for i in range(num_rows):
        A_shifted[i][i] -= eigenvalue

    return null_space(A_shifted)

def eigenvectors(matrix):
    validate_square_matrix(matrix)
    eigenvals = eigenvalues(matrix)
    result = []
    for lam in eigenvals:
        v = eigenvector(matrix, lam)
        result.append((lam, v))
    return result

def diagonalize(matrix):
    num_rows = validate_square_matrix(matrix)
    A = [row[:] for row in matrix]

    values = eigenvectors(A)
    print("Eigenvectors output:", values)

    P_cols = []
    D_vals = []

    for eigenvalue, basis in values:
        for v in basis:
            P_cols.append(v)
            D_vals.append(eigenvalue)

    if len(P_cols) != num_rows:
        raise ValueError("Matrix is not diagonalizable")
    
    P = transpose(P_cols)

    D = [[0.0] * num_rows for _ in range(num_rows)]
    
    for i in range(num_rows):
        D[i][i] = D_vals[i]
    
    P_inv = inverse(P)

    return P, D, P_inv

    
    
    
    
    
    """
    values = eigenvectors(A)

    eigenvectors_T = []
    eigenvalues = []
    multiplicity = []

    for eigenvalue in values:
        eigenvalues.append(eigenvalue[0])
        m = -1
        for eigenvector in eigenvalue[1]:
            m += 1
            eigenvectors_T.append(eigenvector)
        multiplicity.append(m)

    num_eigenvalues = len(eigenvalues)
    num_eigenvectors = len(eigenvectors_T)

    P = transpose(eigenvectors_T)
    D = [[0.0] * num_eigenvectors for _ in range(num_eigenvectors)]

    for i in range(num_eigenvalues):
        for j in range()

    """

def col_space(matrix):
    num_rows, num_cols = validate_matrix(matrix)
    A = [row[:] for row in matrix]
    A1 = rref(A)

    pivot_cols = []
    for row in A1:
        for j in range(num_cols):
            if abs(row[j]) > 1e-10:
                pivot_cols.append(j)
                break

    basis = []
    for col_index in pivot_cols:
        col = [A[i][col_index] for i in range(num_rows)]
        basis.append(col)

    return basis

def row_space(matrix):
    validate_matrix(matrix)
    A = [row[:] for row in matrix]
    A1 = rref(A)

    basis = []
    for row in A1:
        if any(abs(x) > 1e-10 for x in row):
            basis.append(row)

    return basis

def change_of_basis(old_basis, new_basis):
    validate_square_matrix(old_basis, "old_basis")
    validate_square_matrix(new_basis, "new_basis")

    new_inv = inverse(new_basis)

    return matrix_mult(new_inv, old_basis)
