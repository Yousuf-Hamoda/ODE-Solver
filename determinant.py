def minor(term: int, matrix: list, index_x: int, index_y: int):
    # Self Calling Function
    temp_matrix = [row[:] for row in matrix]
    
    if (term > 2):
        for i in range(term):
            del temp_matrix[i][index_y-1]     
            
        del temp_matrix[index_x-1]
                
        if (len(temp_matrix) > 2):
            return det(len(temp_matrix), temp_matrix)

    # If 2x2 matrix, find det
    result: float = (temp_matrix[0][0]*temp_matrix[1][1]) - (temp_matrix[0][1]*temp_matrix[1][0])
    return result

def cofactor(term: int, matrix: list, index_x: int, index_y: int):
    result = (-1)**(index_x + index_y) * minor(term, matrix, index_x, index_y)
    return result
    
def det(term: int, matrix: list):
    result: float = 0.0
    
    for i in range(term):
        result += (matrix[i][0] * cofactor(term, matrix, i+1, 1))
    
    return result
