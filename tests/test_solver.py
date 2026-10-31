import itertools
import math
import random
import sys
from pathlib import Path
import unittest


sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from utils.determinant import det
from services.linalg import solve_ode


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


if __name__ == "__main__":
    unittest.main()
