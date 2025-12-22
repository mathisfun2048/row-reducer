# Input: space = same row

def get_matrix():
    num_rows = int(input("number of rows: "))
    num_cols = int(input("number of cols: "))
    matrix = []

    print("enter row by row, space seperated: \n")
    for _ in range(num_rows):
        r = list(map(float, input(f"Row {_+1}: ").split()))
        if len(r) != num_cols:
            raise ValueError(f"inccorect number of values, each row needs to have {num_cols} numbers")
        matrix.append(r)
        
    return matrix

def rref(matrix):
    copy = [row[:] for row in matrix]
    num_rows = len(copy)
    num_cols = len(copy[0])

    current_row = 0

    for c in range(num_cols):
        pivot_row = None
        for r in range(current_row, num_rows):
            if abs(copy[r][c]) > 1e-10:
                pivot_row = r
                break
            if pivot_row is None:
                continue

        copy[current_row], copy[pivot_row] = copy[pivot_row], copy[current_row]

        pivot = copy[current_row][c]
        copy[current_row] = [x / pivot for x in copy[current_row]]

        for r in range(num_rows):
            if r != current_row:
                factor = copy[r][c]
                copy[r] = [copy[r][i] - factor * copy[current_row][i] for i in range(num_cols)]

        current_row += 1
        if current_row >= num_rows:
            break

    return copy


if __name__ == "__main__":
    matrix = get_matrix()
    result = rref(matrix)

    print("rref: ")
    for row in result:
        print([round(x, 6) for x in row])
