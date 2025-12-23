"""
Test file to verify critical bug fixes
"""

def det_with_pivoting(matrix):
    """Fixed determinant function with proper row swapping"""
    A = [row[:] for row in matrix]
    num_rows = len(A)

    det = 1.0

    for i in range(num_rows):
        # Find pivot (partial pivoting)
        pivot_row = i
        for k in range(i + 1, num_rows):
            if abs(A[k][i]) > abs(A[pivot_row][i]):
                pivot_row = k

        # Swap rows if needed
        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            det *= -1  # Row swap changes sign of determinant

        # Check if matrix is singular
        if abs(A[i][i]) < 1e-10:
            return 0.0

        # Eliminate below pivot
        for j in range(i + 1, num_rows):
            factor = A[j][i] / A[i][i]
            for k in range(i, num_rows):
                A[j][k] -= factor * A[i][k]

        det *= A[i][i]

    return det


def inverse_with_pivoting(matrix):
    """Fixed inverse function with partial pivoting"""
    A = [row[:] for row in matrix]
    num_rows = len(A)

    # Create augmented matrix [A | I]
    augment = [matrix[i][:] + [1 if i == j else 0 for j in range(num_rows)] for i in range(num_rows)]

    # Forward elimination with partial pivoting
    for i in range(num_rows):
        # Find pivot row
        pivot_row = i
        for k in range(i + 1, num_rows):
            if abs(augment[k][i]) > abs(augment[pivot_row][i]):
                pivot_row = k

        # Swap rows if needed
        if pivot_row != i:
            augment[i], augment[pivot_row] = augment[pivot_row], augment[i]

        # Check if matrix is singular
        pivot = augment[i][i]
        if abs(pivot) < 1e-10:
            raise ValueError("matrix is singular")

        # Scale pivot row
        for j in range(2 * num_rows):
            augment[i][j] /= pivot

        # Eliminate column
        for k in range(num_rows):
            if k != i:
                factor = augment[k][i]
                for j in range(2 * num_rows):
                    augment[k][j] -= factor * augment[i][j]

    return [[augment[i][j] for j in range(num_rows, 2 * num_rows)] for i in range(num_rows)]


def lu_with_check(matrix):
    """Fixed LU decomposition with division by zero check"""
    A = [row[:] for row in matrix]
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    if num_rows != num_cols:
        raise ValueError("matrix must be square")

    L = [[0.0] * num_cols for _ in range(num_rows)]
    U = [[0.0] * num_cols for _ in range(num_rows)]

    for i in range(num_rows):
        # Compute U[i][j] for j >= i
        for j in range(i, num_rows):
            sum_val = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - sum_val

        # Check for zero pivot
        if abs(U[i][i]) < 1e-10:
            raise ValueError("Matrix requires pivoting for LU decomposition (zero pivot encountered)")

        # Compute L[j][i] for j >= i
        for j in range(i, num_rows):
            if i == j:
                L[i][j] = 1.0
            else:
                sum_val = sum(L[j][k] * U[k][i] for k in range(i))
                L[j][i] = (A[j][i] - sum_val) / U[i][i]

    return L, U


# Test cases
print("Testing determinant fix:")
print("-" * 50)

# Test 1: Matrix with zero on diagonal but non-zero determinant
test1 = [[0, 1], [1, 0]]
print(f"Matrix: {test1}")
print(f"Determinant: {det_with_pivoting(test1)}")
print(f"Expected: -1.0")
print()

# Test 2: Larger matrix needing pivoting
test2 = [[0, 1, 2], [1, 0, 3], [4, 5, 6]]
print(f"Matrix: {test2}")
print(f"Determinant: {det_with_pivoting(test2)}")
# det = -1*(1*6 - 3*5) + 2*(1*5 - 0*4) = -1*(-9) + 2*5 = 9 + 10 = 19
# After first swap: [[1,0,3],[0,1,2],[4,5,6]], det *= -1
# Then standard elimination
print()

print("\nTesting inverse fix:")
print("-" * 50)

# Test 3: Matrix that is its own inverse
test3 = [[0, 1], [1, 0]]
print(f"Matrix: {test3}")
try:
    inv = inverse_with_pivoting(test3)
    print(f"Inverse: {inv}")
    print(f"Expected: [[0, 1], [1, 0]]")
except Exception as e:
    print(f"Error: {e}")
print()

# Test 4: Regular matrix
test4 = [[1, 2], [3, 4]]
print(f"Matrix: {test4}")
inv4 = inverse_with_pivoting(test4)
print(f"Inverse: {[[round(x, 6) for x in row] for row in inv4]}")
print(f"Expected: [[-2.0, 1.0], [1.5, -0.5]]")
print()

print("\nTesting LU fix:")
print("-" * 50)

# Test 5: Matrix that fails without pivoting
test5 = [[1, 1], [1, 1]]  # Singular matrix
print(f"Matrix: {test5}")
try:
    L, U = lu_with_check(test5)
    print("LU succeeded (unexpected)")
except ValueError as e:
    print(f"Correctly raised error: {e}")
print()

# Test 6: Regular matrix
test6 = [[2, 1], [1, 2]]
print(f"Matrix: {test6}")
try:
    L, U = lu_with_check(test6)
    print(f"L: {[[round(x, 6) for x in row] for row in L]}")
    print(f"U: {[[round(x, 6) for x in row] for row in U]}")
except ValueError as e:
    print(f"Error: {e}")
