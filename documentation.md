# Scaler / Single Value Functions 

## det(A)
### Input: matrix
### Output: determinant of matrix

## trace(A)
### Input: matrix
### Output: trace of matrix

## rank(A)
### Input: matrix
### Output: rank of matrix

## null(A)
### Input: matrix
### Output: nullity of matrix

## magnitude(v)
### Input: vector
### Output: norm of vector

## dot_product(v1, v2)
### Input: 2 vectors
### Output: dot product of vectors

## lin_ind(A)
### Input: matrix
### Output: whether the cols are linearly independent or not


# Matrix / Vector Functions

## rref(A)
### Input: matrix
### Output: matrix in reduced row echelon form

## inverse(A)
### Input: matrix
### Output: inverse of the matrix

## transpose(A)
### Input: matrix
### Output: transpose of the matrix

## cross(v1, v2)
### Input: 2 3-D vectors
### Output: cross product of the vectors

## projection(a, v)
### Input: 2 vectors
### Output: projection of a onto v

## matrix_mult(A, B)
### Input: 2 matricies
### Output: AB *not BA*

## solve_system(A, b)
### Input: matrix and vector
### Output: solves Ax=b

## eigenvectors(A)
### Input: matrix
### Output: eigenvalues and corresponding eigenvectors


# Basis Functions

## null_space(A)
### Input: matrix
### Output: null space basis as row vectors

## col_space(A)
### Input: matrix
### Output: col space as row vectors

## row_space(A)
### Input: matrix
### Output: row space as row vectors

## change_of_basis(old, new)
### Input: 2 matricies
### Output: change of basis matrix


# Decomposition Functions
## lu(A)
### Input: matrix
### Output: lower-upper decomposition

## qr(A)
### Input: matrix
### Output: orthogonal-upper right triangular decomposition

## diagonalize(A)
### Input: matrix
### Output: PDP-1, used for repeated exponentiation