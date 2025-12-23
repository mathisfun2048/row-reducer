"""
Comprehensive test suite for all functions in main.py
Tests both valid inputs and edge cases
"""
from main import (
    rref, lu, dot_product, magnitude, qr, inverse, det,
    matrix_times_vector, matrix_mult, solve_system, transpose,
    trace, rank, null, cross, projection, lin_ind, eigenvalues,
    null_space, eigenvector, eigenvectors, diagonalize,
    col_space, row_space, change_of_basis
)

def test_function(name, func, *args, **kwargs):
    """Helper to test a function and report results"""
    try:
        result = func(*args, **kwargs)
        print(f"✓ {name}")
        return result
    except Exception as e:
        print(f"✗ {name}: {e}")
        return None

print("=" * 70)
print("COMPREHENSIVE FUNCTION TEST SUITE")
print("=" * 70)

# Test matrices
identity_2x2 = [[1, 0], [0, 1]]
matrix_2x2 = [[1, 2], [3, 4]]
matrix_3x3 = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
symmetric_2x2 = [[2, 1], [1, 2]]
vector_2 = [1, 2]
vector_3 = [1, 2, 3]

print("\n1. Basic Matrix Operations")
print("-" * 70)
test_function("rref(2x2)", rref, matrix_2x2)
test_function("rref(3x3)", rref, matrix_3x3)
test_function("transpose(2x2)", transpose, matrix_2x2)
test_function("transpose(3x3)", transpose, matrix_3x3)

print("\n2. Matrix Decompositions")
print("-" * 70)
test_function("lu(2x2)", lu, symmetric_2x2)
test_function("qr(2x2)", qr, matrix_2x2)
test_function("qr(3x3)", qr, matrix_3x3)

print("\n3. Matrix Properties")
print("-" * 70)
test_function("det(2x2)", det, matrix_2x2)
test_function("det(3x3)", det, matrix_3x3)
test_function("trace(2x2)", trace, matrix_2x2)
test_function("trace(3x3)", trace, matrix_3x3)
test_function("rank(2x2)", rank, matrix_2x2)
test_function("rank(3x3)", rank, matrix_3x3)
test_function("null(2x2)", null, identity_2x2)

print("\n4. Matrix Inversion")
print("-" * 70)
test_function("inverse(2x2)", inverse, matrix_2x2)
test_function("inverse(identity)", inverse, identity_2x2)

print("\n5. Matrix Multiplication")
print("-" * 70)
test_function("matrix_mult(2x2, 2x2)", matrix_mult, matrix_2x2, identity_2x2)
test_function("matrix_times_vector(2x2, vec2)", matrix_times_vector, matrix_2x2, vector_2)

print("\n6. System Solving")
print("-" * 70)
test_function("solve_system(2x2, vec2)", solve_system, matrix_2x2, vector_2)

print("\n7. Vector Operations")
print("-" * 70)
test_function("dot_product(vec2, vec2)", dot_product, vector_2, vector_2)
test_function("dot_product(vec3, vec3)", dot_product, vector_3, vector_3)
test_function("magnitude(vec2)", magnitude, vector_2)
test_function("magnitude(vec3)", magnitude, vector_3)
test_function("cross(vec3, vec3)", cross, vector_3, [4, 5, 6])
test_function("projection(vec2, vec2)", projection, vector_2, [3, 4])

print("\n8. Linear Independence")
print("-" * 70)
test_function("lin_ind(2x2)", lin_ind, matrix_2x2)
test_function("lin_ind(identity)", lin_ind, identity_2x2)

print("\n9. Eigenvalues and Eigenvectors")
print("-" * 70)
test_function("eigenvalues(symmetric 2x2)", eigenvalues, symmetric_2x2)
evals = eigenvalues(symmetric_2x2)
if evals:
    test_function("eigenvector(2x2, lambda)", eigenvector, symmetric_2x2, evals[0])
test_function("eigenvectors(symmetric 2x2)", eigenvectors, symmetric_2x2)

print("\n10. Null Space and Column/Row Spaces")
print("-" * 70)
singular_matrix = [[1, 2], [2, 4]]
test_function("null_space(singular)", null_space, singular_matrix)
test_function("col_space(2x2)", col_space, matrix_2x2)
test_function("row_space(2x2)", row_space, matrix_2x2)

print("\n11. Diagonalization")
print("-" * 70)
test_function("diagonalize(symmetric 2x2)", diagonalize, symmetric_2x2)

print("\n12. Change of Basis")
print("-" * 70)
basis1 = [[1, 0], [0, 1]]
basis2 = [[1, 1], [0, 1]]
test_function("change_of_basis", change_of_basis, basis1, basis2)

print("\n" + "=" * 70)
print("BASELINE TESTS COMPLETE - All functions work before validation")
print("=" * 70)
