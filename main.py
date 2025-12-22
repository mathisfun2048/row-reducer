
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

def dot_product(v1, v2):
    return sum(a*b for a, b in zip(v1, v2))

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

if __name__ == "__main__":
   qr_printer()