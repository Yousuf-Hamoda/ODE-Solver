# Determinant calculator using cofactor expansion.
# Matrix entries may be plain numbers OR zero-argument callables (for symbolic use).

def minor(matrix: list, row: int, col: int) -> float:
    # Return the minor of `matrix` obtained by deleting `row` and `col` (0-indexed).
    sub = []
    
    for r in range(len(matrix)):        
        if r != row:
            new_row = []
            
            for c in range(len(matrix[r])):
                if c != col:
                    value = matrix[r][c]
                    new_row.append(value)
    
            sub.append(new_row)
    
    return det(sub) 
~
def cofactor(term: int, matrix: list, row: int, col: int):
    return  (-1)**(row + col) * minor(matrix, row, col)
 
def det(matrix: list) -> float:
    # Recursive cofactor-expansion determinant (no external libraries).
    # Expands along column 0.
    
    n = len(matrix)
 
    if n == 1:
        return _val(matrix[0][0])
 
    if n == 2:
        return matrix[0][0] * matrix[1][1] - \
               matrix[0][1] * matrix[1][0]
 
    result = 0.0
    for i in range(n):
        result += matrix[i][0] * cofactor(matrix, i, 0)
    return result
 
