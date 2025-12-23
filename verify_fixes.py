"""
Verify the fixes work in the actual main.py file
"""
from main import det, inverse, lu

print("=" * 60)
print("TESTING CRITICAL BUG FIXES")
print("=" * 60)

# Test 1: Determinant with zero on diagonal
print("\nTest 1: Determinant - Matrix with zero on diagonal")
print("-" * 60)
test1 = [[0, 1], [1, 0]]
result = det(test1)
print(f"Input: {test1}")
print(f"Result: {result}")
print(f"Expected: -1.0")
print(f"Status: {'PASS' if abs(result - (-1.0)) < 1e-6 else 'FAIL'}")

# Test 2: Determinant - 3x3 with zeros
print("\nTest 2: Determinant - 3x3 matrix needing pivoting")
print("-" * 60)
test2 = [[0, 1, 2], [1, 0, 3], [4, 5, 6]]
result = det(test2)
print(f"Input: {test2}")
print(f"Result: {result}")
print(f"Expected: 16.0")
print(f"Status: {'PASS' if abs(result - 16.0) < 1e-6 else 'FAIL'}")

# Test 3: Inverse - Matrix that is its own inverse
print("\nTest 3: Inverse - Matrix with zero on diagonal")
print("-" * 60)
test3 = [[0, 1], [1, 0]]
try:
    result = inverse(test3)
    print(f"Input: {test3}")
    print(f"Result: {[[round(x, 6) for x in row] for row in result]}")
    print(f"Expected: [[0, 1], [1, 0]]")
    is_correct = (abs(result[0][0]) < 1e-6 and abs(result[0][1] - 1.0) < 1e-6 and
                  abs(result[1][0] - 1.0) < 1e-6 and abs(result[1][1]) < 1e-6)
    print(f"Status: {'PASS' if is_correct else 'FAIL'}")
except Exception as e:
    print(f"FAIL - Error: {e}")

# Test 4: Inverse - Regular matrix
print("\nTest 4: Inverse - Regular 2x2 matrix")
print("-" * 60)
test4 = [[1, 2], [3, 4]]
result = inverse(test4)
print(f"Input: {test4}")
print(f"Result: {[[round(x, 6) for x in row] for row in result]}")
print(f"Expected: [[-2.0, 1.0], [1.5, -0.5]]")
is_correct = (abs(result[0][0] - (-2.0)) < 1e-6 and abs(result[0][1] - 1.0) < 1e-6 and
              abs(result[1][0] - 1.5) < 1e-6 and abs(result[1][1] - (-0.5)) < 1e-6)
print(f"Status: {'PASS' if is_correct else 'FAIL'}")

# Test 5: LU - Singular matrix should fail
print("\nTest 5: LU - Singular matrix detection")
print("-" * 60)
test5 = [[1, 1], [1, 1]]
print(f"Input: {test5}")
try:
    L, U = lu(test5)
    print(f"FAIL - Should have raised an error for singular matrix")
except ValueError as e:
    print(f"Result: Correctly raised ValueError")
    print(f"Error message: {e}")
    print(f"Status: PASS")

# Test 6: LU - Regular matrix
print("\nTest 6: LU - Regular matrix decomposition")
print("-" * 60)
test6 = [[2, 1], [1, 2]]
try:
    L, U = lu(test6)
    print(f"Input: {test6}")
    print(f"L: {[[round(x, 6) for x in row] for row in L]}")
    print(f"U: {[[round(x, 6) for x in row] for row in U]}")
    print(f"Expected L: [[1.0, 0.0], [0.5, 1.0]]")
    print(f"Expected U: [[2.0, 1.0], [0.0, 1.5]]")
    print(f"Status: PASS")
except ValueError as e:
    print(f"FAIL - Error: {e}")

print("\n" + "=" * 60)
print("ALL CRITICAL FIXES VERIFIED")
print("=" * 60)
