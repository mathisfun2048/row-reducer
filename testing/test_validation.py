"""
Test that validation properly catches invalid inputs
"""
from main import (
    rref, lu, dot_product, magnitude, qr, inverse, det,
    matrix_times_vector, matrix_mult, solve_system, transpose,
    trace, rank, null, cross, projection, eigenvalues, diagonalize
)

def test_error(name, func, args):
    """Test that a function properly raises an error"""
    try:
        result = func(*args)
        print(f"✗ {name}: Should have raised ValueError")
        return False
    except ValueError as e:
        print(f"✓ {name}: {e}")
        return True
    except Exception as e:
        print(f"✗ {name}: Wrong exception type: {type(e).__name__}: {e}")
        return False

print("=" * 70)
print("VALIDATION TESTS - Edge Cases and Invalid Inputs")
print("=" * 70)

print("\n1. Empty Matrix Tests")
print("-" * 70)
test_error("rref(empty matrix)", rref, ([],))
test_error("rref(empty rows)", rref, ([[]],))
test_error("det(empty)", det, ([],))
test_error("inverse(empty)", inverse, ([],))

print("\n2. Inconsistent Dimensions")
print("-" * 70)
test_error("rref(inconsistent rows)", rref, ([[1, 2], [3, 4, 5]],))
test_error("matrix_mult(inconsistent)", matrix_mult, ([[1, 2], [3]], [[1], [2]]))

print("\n3. Square Matrix Requirements")
print("-" * 70)
test_error("lu(non-square)", lu, ([[1, 2, 3], [4, 5, 6]],))
test_error("det(non-square)", det, ([[1, 2, 3], [4, 5, 6]],))
test_error("inverse(non-square)", inverse, ([[1, 2, 3], [4, 5, 6]],))
test_error("trace(non-square)", trace, ([[1, 2, 3], [4, 5, 6]],))
test_error("eigenvalues(non-square)", eigenvalues, ([[1, 2, 3], [4, 5, 6]],))

print("\n4. Vector Validation")
print("-" * 70)
test_error("dot_product(empty)", dot_product, ([], [1, 2]))
test_error("dot_product(mismatched length)", dot_product, ([1, 2], [1, 2, 3]))
test_error("magnitude(empty)", magnitude, ([],))
test_error("cross(not 3D)", cross, ([1, 2], [3, 4]))
test_error("cross(empty)", cross, ([], []))

print("\n5. Matrix-Vector Compatibility")
print("-" * 70)
test_error("matrix_times_vector(wrong size)", matrix_times_vector, ([[1, 2], [3, 4]], [1, 2, 3]))
test_error("solve_system(wrong size)", solve_system, ([[1, 2], [3, 4]], [1, 2, 3]))

print("\n6. Matrix Multiplication Compatibility")
print("-" * 70)
test_error("matrix_mult(incompatible)", matrix_mult, ([[1, 2], [3, 4]], [[1], [2], [3]]))

print("\n7. Zero Vector Projection")
print("-" * 70)
test_error("projection(onto zero vector)", projection, ([1, 2], [0, 0]))

print("\n8. Singular Matrices")
print("-" * 70)
test_error("inverse(singular)", inverse, ([[1, 2], [2, 4]],))
test_error("lu(needs pivoting)", lu, ([[1, 1], [1, 1]],))

print("\n" + "=" * 70)
print("VALIDATION TESTS COMPLETE")
print("=" * 70)
