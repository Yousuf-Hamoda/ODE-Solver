import itertools
import math
import random
import sys
from pathlib import Path
import unittest


sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from utils.determinant import det
from services.linalg import eigensystem, solve_ode


def permutation_det(matrix):
    # Leibniz formula, used only as an independent reference.
    n = len(matrix)
    total = 0.0
    for perm in itertools.permutations(range(n)):
        inversions = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
        total += (-1) ** inversions * math.prod(matrix[i][perm[i]] for i in range(n))
    return total


class DeterminantTests(unittest.TestCase):
    def test_matches_reference_for_sizes_1_to_6(self):
        rng = random.Random(1)
        for n in range(1, 7):
            for _ in range(10):
                m = [[rng.uniform(-5, 5) for _ in range(n)] for _ in range(n)]
                expected = permutation_det(m)
                self.assertAlmostEqual(det(m), expected, delta=1e-9 * (1 + abs(expected)))


class SolveOdeTests(unittest.TestCase):
    def assertSolutionClose(self, actual, expected):
        for row, exp_row in zip(actual, expected):
            for value, exp in zip(row, exp_row):
                self.assertAlmostEqual(value, exp, places=9)

    def test_diagonal_3x3(self):
        ts = [0.0, 0.5, 1.0]
        actual = solve_ode([[1, 0, 0], [0, 2, 0], [0, 0, 3]], [1, 1, 1], ts)
        expected = [[math.exp(k * t) for k in (1, 2, 3)] for t in ts]
        self.assertSolutionClose(actual, expected)

    def test_3d_spiral_preset(self):
        # x' = -x + 2y, y' = -2x - y, z' = -z/2 with x0 = (1, 0, 1)
        ts = [0.0, 0.7, 2.0]
        actual = solve_ode([[-1, 2, 0], [-2, -1, 0], [0, 0, -0.5]], [1, 0, 1], ts)
        expected = [
            [math.exp(-t) * math.cos(2 * t), -math.exp(-t) * math.sin(2 * t), math.exp(-0.5 * t)]
            for t in ts
        ]
        self.assertSolutionClose(actual, expected)

    def test_random_systems_up_to_8x8_match_rk4(self):
        # Sizes >= 5 used to return wrong eigenvectors (and so wrong x(t))
        # because the approximate eigenvalue made A - λI look nonsingular.
        rng = random.Random(3)
        for n in range(3, 9):
            for _ in range(3):
                A = [[rng.uniform(-2, 2) for _ in range(n)] for _ in range(n)]
                x0 = [rng.uniform(-1, 1) for _ in range(n)]
                actual = solve_ode(A, x0, [1.0])[0]
                expected = rk4(A, x0, 1.0, 1000)
                scale = 1 + max(abs(v) for v in expected)
                for value, exp in zip(actual, expected):
                    self.assertAlmostEqual(value, exp, delta=1e-8 * scale)


class EigensystemTests(unittest.TestCase):
    def test_eigenpairs_satisfy_definition_up_to_8x8(self):
        rng = random.Random(7)
        for n in range(2, 9):
            for _ in range(10):
                A = [[rng.uniform(-5, 5) for _ in range(n)] for _ in range(n)]
                for lam, v in zip(*eigensystem(A)):
                    self.assertAlmostEqual(sum(abs(x) ** 2 for x in v), 1.0, places=9)
                    for i in range(n):
                        residual = sum(A[i][j] * v[j] for j in range(n)) - lam * v[i]
                        self.assertLess(abs(residual), 1e-8)


def rk4(A, x0, T, steps):
    # Independent numerical reference for x' = Ax.
    n = len(A)
    x = [float(v) for v in x0]
    h = T / steps

    def f(v):
        return [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]

    for _ in range(steps):
        k1 = f(x)
        k2 = f([x[i] + h / 2 * k1[i] for i in range(n)])
        k3 = f([x[i] + h / 2 * k2[i] for i in range(n)])
        k4 = f([x[i] + h * k3[i] for i in range(n)])
        x = [x[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(n)]
    return x


if __name__ == "__main__":
    unittest.main()
