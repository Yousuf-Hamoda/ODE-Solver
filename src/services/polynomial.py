# Builds coefficients via finite differences (no symbolic algebra needed).

from determinant import det

def char_poly_coeffs(A: list) -> list:
    n = len(A)
    num_points = n + 1
    xs = [float(k) for k in range(num_points)]

    def eval_char(lam: float) -> float:
        # Evaluate det(A - lam*I).
        shifted = []
        for i in range(n):
            row_temp = []
            for j in range(n):
                row_temp.append(A[i][j] - (lam if i == j else 0.0))

            shifted.append(row_temp)
        return det(shifted)

    ys = [eval_char(x) for x in xs]

    # Newton divided differences → coefficients in the Newton basis, then convert to standard monomial basis.
    coeffs_newton = _divided_differences(xs, ys)
    poly = _newton_to_standard(coeffs_newton, xs)
    
    # Return highest-degree first: [a_n, a_{n-1}, ..., a_0]
    return list(reversed(poly))

def _divided_differences(xs: list, ys: list) -> list:
    # Return the leading divided-difference coefficients.
    n = len(xs)
    table = ys[:]
    coeffs = [table[0]]
    
    for j in range(1, n):
        new_table = []

        for i in range(n - j):
            new_table.append((table[i + 1] - table[i]) / (xs[i + j] - xs[i]))

        table = new_table
        coeffs.append(table[0])
    
    return coeffs

def _newton_to_standard(coeffs: list, xs: list) -> list:
    # Convert Newton form  Σ c_k * (λ-x0)(λ-x1)...(λ-x_{k-1}) to standard form  Σ a_k * λ^k.
    # Returns list where index k → coefficient of λ^k.
    
    n = len(coeffs)
    # Start with just the constant c_{n-1}
    result = [0.0] * n
    result[0] = coeffs[n - 1]

    for k in range(n - 2, -1, -1):
        # Multiply current poly by (λ - x_k): shift up and subtract x_k
        new_result = [0.0] * n
        for i in range(n - 1):
            new_result[i + 1] += result[i]
            new_result[i]     -= xs[k] * result[i]
        result = new_result
        result[0] += coeffs[k]

    return result