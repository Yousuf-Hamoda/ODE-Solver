# Solves  x'(t) = A x(t),  x(0) = x0 using the eigendecomposition  x(t) = Σ c_k * v_k * e^(λ_k * t).

# All arithmetic is pure Python (complex numbers built-in).

import cmath
import math
from services.polynomial import char_poly_coeffs
from services.root_solver import find_roots, clean_roots
from utils.gauss_elim import gauss_eliminate


def _null_vector(A: list, lam: complex, iterations: int = 3) -> list:
    # Return a unit vector v such that (A - λI)v ≈ 0, via inverse iteration.
    #
    # λ is only an approximate root, so (A - λI) is nearly (not exactly)
    # singular and elimination will not reliably expose a free variable.
    # Inverse iteration instead solves (A - λI)y = v repeatedly: the
    # component of v along the eigenvector is amplified by 1/|error in λ|,
    # so a few solves converge to the eigenvector.

    n = len(A)
    scale = max(1.0, max(abs(A[i][j]) for i in range(n) for j in range(n)))
    tiny = 1e-14 * scale

    # LU factorisation of (A - λI) with partial pivoting.
    LU = [
        [complex(A[i][j]) - (lam if i == j else 0) for j in range(n)]
        for i in range(n)
    ]
    perm = list(range(n))
    for col in range(n):
        best = max(range(col, n), key=lambda r: abs(LU[r][col]))
        LU[col], LU[best] = LU[best], LU[col]
        perm[col], perm[best] = perm[best], perm[col]
        if abs(LU[col][col]) < tiny:
            LU[col][col] = complex(tiny)    # exactly singular: nudge the pivot
        for r in range(col + 1, n):
            factor = LU[r][col] / LU[col][col]
            LU[r][col] = factor
            for c in range(col + 1, n):
                LU[r][c] -= factor * LU[col][c]

    def lu_solve(b):
        y = [b[perm[i]] for i in range(n)]
        for i in range(n):
            y[i] -= sum(LU[i][k] * y[k] for k in range(i))
        for i in reversed(range(n)):
            y[i] = (y[i] - sum(LU[i][k] * y[k] for k in range(i + 1, n))) / LU[i][i]
        return y

    # Start from a vector unlikely to be orthogonal to the eigenvector.
    v = [complex(1.0 + 0.1 * i) for i in range(n)]
    for _ in range(iterations):
        v = lu_solve(v)
        norm = math.sqrt(sum(abs(x) ** 2 for x in v))
        v = [x / norm for x in v]

    # Fix the phase so the largest component is real and positive; this
    # keeps the displayed eigenvectors stable and readable.
    big = max(v, key=abs)
    phase = abs(big) / big
    return [x * phase for x in v]


# ---------------------------------------------------------------------------
# Eigensystem
# ---------------------------------------------------------------------------

def eigensystem(A: list):
    """
    Return (eigenvalues, eigenvectors) for matrix A.
    eigenvalues : list of complex
    eigenvectors: list of lists of complex  (one per eigenvalue, same order)
    """
    coeffs = char_poly_coeffs(A)
    raw_roots = find_roots(coeffs)
    eigenvalues = clean_roots(raw_roots)
    eigenvectors = [_null_vector(A, lam) for lam in eigenvalues]
    return eigenvalues, eigenvectors


# ---------------------------------------------------------------------------
# Solve for constants c_k given x(0) = x0
# ---------------------------------------------------------------------------

def _solve_constants(eigenvectors: list, x0: list) -> list:
    """
    Solve  V * c = x0  where V columns are eigenvectors.
    Returns c (list of complex).
    """
    n = len(x0)
    # Build augmented matrix [V | x0]
    M = [
        [eigenvectors[j][i] for j in range(n)] + [complex(x0[i])]
        for i in range(n)
    ]
    M = gauss_eliminate(M)

    c = [complex(0)] * n
    for i, row in enumerate(M):
        # Find pivot column
        for col in range(n):
            if abs(row[col] - 1.0) < 1e-8:
                c[col] = row[n]   # augment value
                break
    return c


# ---------------------------------------------------------------------------
# Evaluate x(t)
# ---------------------------------------------------------------------------

def solve_ode(A: list, x0: list, t_values: list) -> list:
    """
    Solve x'(t) = A x(t), x(0) = x0.

    Parameters
    ----------
    A        : n×n coefficient matrix (list of lists of float)
    x0       : initial condition vector (list of float, length n)
    t_values : list of time points at which to evaluate x(t)

    Returns
    -------
    List of solution vectors (one per t value).
    Each solution vector contains real-valued floats
    (imaginary parts from conjugate pairs cancel; we strip them).
    """
    eigenvalues, eigenvectors = eigensystem(A)
    constants = _solve_constants(eigenvectors, x0)
    n = len(x0)

    results = []
    for t in t_values:
        x = [complex(0)] * n
        for k in range(n):
            lam = eigenvalues[k]
            c_k = constants[k]
            v_k = eigenvectors[k]
            scalar = c_k * cmath.exp(lam * t)
            for i in range(n):
                x[i] += scalar * v_k[i]
        # Imaginary parts should be negligible for real systems
        results.append([xi.real for xi in x])

    return results