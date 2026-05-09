# Solves  x'(t) = A x(t),  x(0) = x0 using the eigendecomposition  x(t) = Σ c_k * v_k * e^(λ_k * t).

# All arithmetic is pure Python (complex numbers built-in).

import cmath
import math
from services.polynomial import char_poly_coeffs
from services.root_solver import find_roots, clean_roots
from utils.gauss_elim import gauss_eliminate


def _null_vector(A: list, lam: complex) -> list:
    # Return a non-trivial vector v such that (A - λI)v ≈ 0.
    # Uses Gaussian elimination on (A - λI | 0) then back-substitutes.
    
    n = len(A)
    # Build (A - λI) augmented with zero column
    M = [
        [complex(A[i][j]) - (lam if i == j else 0) for j in range(n)] + [complex(0)]
        for i in range(n)
    ]
    M = gauss_eliminate(M)

    # Identify free variables (columns with no pivot)
    pivot_cols = []
    for row in M:
        for c in range(n):
            if abs(row[c] - 1.0) < 1e-8 and all(abs(row[cc]) < 1e-8 for cc in range(n) if cc != c):
                pivot_cols.append(c)
                break

    free_cols = [c for c in range(n) if c not in pivot_cols]
    if not free_cols:
        free_cols = [n - 1]     # fallback

    # Set free variable = 1, solve for pivot variables
    v = [complex(0)] * n
    for fc in free_cols:
        v[fc] = complex(1)

    for row in reversed(M):
        # Find pivot of this row
        pc = -1
        for c in range(n):
            if abs(row[c] - 1.0) < 1e-8:
                pc = c
                break
        if pc == -1:
            continue
        v[pc] = -sum(row[c] * v[c] for c in range(n) if c != pc)

    # Normalise
    norm = math.sqrt(sum(abs(x) ** 2 for x in v))
    if norm > 1e-12:
        v = [x / norm for x in v]

    return v


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