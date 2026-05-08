# Finds all roots (real and complex) via the Durand-Kerner method.

import cmath
import math

def find_roots(coeffs: list, tol: float = 1e-10, max_iter: int = 1000) -> list:
    # Find all roots of the polynomial with given coefficients (highest degree first).
    # Uses the Durand-Kerner / Weierstrass iteration.
    # Returns a list of complex numbers.

    # Normalise so leading coefficient is 1
    lc = coeffs[0]
    coeffs = [c / lc for c in coeffs]
    n = len(coeffs) - 1   # degree

    if n == 0:
        return []
    if n == 1:
        return [complex(-coeffs[1])]

    # Initial guesses spread on a circle in the complex plane
    r = 1.0 + max(abs(c) for c in coeffs[1:]) ** (1.0 / n)
    roots = [
        cmath.rect(r, 2 * math.pi * k / n) * complex(0.4, 0.9) ** k
        for k in range(n)
    ]

    def poly_eval(z):
        val = complex(0)
        for c in coeffs:
            val = val * z + c
        return val

    for _ in range(max_iter):
        new_roots = []
        max_change = 0.0
        for i, zi in enumerate(roots):
            denom = complex(1)
            for j, zj in enumerate(roots):
                if i != j:
                    denom *= (zi - zj)
            if abs(denom) < 1e-30:
                new_roots.append(zi)
                continue
            delta = poly_eval(zi) / denom
            new_roots.append(zi - delta)
            max_change = max(max_change, abs(delta))
        roots = new_roots
        if max_change < tol:
            break

    return roots

def clean_roots(roots: list, tol: float = 1e-8) -> list:
    # Round negligible imaginary/real parts to zero for display.
    cleaned = []
    for r in roots:
        re = r.real if abs(r.real) > tol else 0.0
        im = r.imag if abs(r.imag) > tol else 0.0
        cleaned.append(complex(re, im))
    return cleaned