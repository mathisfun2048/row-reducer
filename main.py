# Input: space = same row

def get_matrix():
    r = int(input("number of rows: "))
    c = int(input("number of cols: "))
    matrix = []

    print("enter row by row, space seperated: \n")
    for _ in range(r):
        row = list(map(float, input(f"Row {_+1}: ").split()))
        if len(row) != c:
            raise ValueError(f"inccorect number of values, each row needs to have {c} numbers")
        matrix.append(row)
        
    return matrix