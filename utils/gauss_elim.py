import cmath
import math

# Gaussian elimination (complex entries)
def gauss_eliminate(M: list) -> list:
    # Row-reduce augmented matrix M (list of lists of complex) in-place.
    # Returns the row-echelon form.
    M = [row[:] for row in M]   # copy
    n_rows = len(M)
    n_cols = len(M[0])
    pivot_row = 0

    for col in range(n_cols - 1):          # skip augment column
        # Find pivot
        best = pivot_row
        for r in range(pivot_row + 1, n_rows):
            if abs(M[r][col]) > abs(M[best][col]):
                best = r
        if abs(M[best][col]) < 1e-12:
            continue
        M[pivot_row], M[best] = M[best], M[pivot_row]

        # Eliminate below
        for r in range(n_rows):
            if r != pivot_row and abs(M[r][col]) > 1e-12:
                factor = M[r][col] / M[pivot_row][col]
                for c in range(n_cols):
                    M[r][c] -= factor * M[pivot_row][c]

        # Scale pivot row
        scale = M[pivot_row][col]
        for c in range(n_cols):
            M[pivot_row][c] /= scale

        pivot_row += 1

    return M