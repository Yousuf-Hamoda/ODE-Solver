# main.py  —  Terminal interface for the pure-Python ODE solver.

# Solves the linear system  x'(t) = A·x(t)  given:
#   - an n×n coefficient matrix A
#   - an initial condition vector x(0)
#   - a time range and optional specific t values to evaluate

# Run:
#     python main.py

import sys
import os

# Allow main.py to find sibling modules (determinant, polynomial, linalg)
# regardless of where the script is launched from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.linalg import solve_ode, eigensystem


# ─── Formatting helpers ───────────────────────────────────────────────────────

def fmt_number(value: float, digits: int = 6) -> str:
    # Format a float, collapsing near-zero values to 0.
    if abs(value) < 1e-10:
        return "0"
    return f"{value:.{digits}f}".rstrip("0").rstrip(".")


def fmt_complex(z: complex) -> str:
    # Format a complex number as  a + bi  or  a  or  bi.
    re, im = z.real, z.imag
    pure_re = abs(im) < 1e-8
    pure_im = abs(re) < 1e-8
    sign    = "-" if im < -1e-8 else "+"

    if pure_re:
        return fmt_number(re)
    if pure_im:
        return f"{fmt_number(im)}i"
    return f"{fmt_number(re)} {sign} {fmt_number(abs(im))}i"


def fmt_vector(values, formatter=fmt_number) -> str:
    # Format a list of numbers as  [ v1,  v2,  v3 ].
    return "[ " + ",  ".join(formatter(v) for v in values) + " ]"


# ─── Input helpers ────────────────────────────────────────────────────────────

def prompt(msg: str) -> str:
    # Print a prompt and return stripped input, exiting cleanly on Ctrl-C.
    try:
        return input(msg).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        sys.exit(0)


def read_int(msg: str, min_val: int = 1) -> int:
    while True:
        raw = prompt(msg)
        try:
            value = int(raw)
            if value >= min_val:
                return value
            print(f"  Please enter an integer ≥ {min_val}.")
        except ValueError:
            print("  Invalid input — please enter a whole number.")


def read_float(msg: str) -> float:
    while True:
        raw = prompt(msg)
        try:
            return float(raw)
        except ValueError:
            print("  Invalid input — please enter a number.")


def read_row(msg: str, expected_len: int) -> list:
    # Read a space-separated row of floats, re-prompting on bad input.
    while True:
        raw = prompt(msg)
        try:
            values = list(map(float, raw.split()))
            if len(values) != expected_len:
                print(f"  Expected {expected_len} values, got {len(values)}. Try again.")
                continue
            return values
        except ValueError:
            print("  Could not parse numbers. Use spaces between values, e.g.:  1 0 -2")


# ─── Display helpers ──────────────────────────────────────────────────────────

DIVIDER     = "─" * 52
THIN_DIVIDER = "·" * 52


def print_section(title: str):
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


def print_matrix(matrix: list, label: str = "A"):
    n = len(matrix)
    col_w = 10
    print(f"\n  {label}:")
    for i, row in enumerate(matrix):
        prefix = "  ⌈" if i == 0 else ("  ⌊" if i == n - 1 else "  │")
        suffix = "⌉" if i == 0 else ("⌋" if i == n - 1 else "│")
        row_str = "  ".join(f"{v:>{col_w}.4f}" for v in row)
        print(f"  {prefix}  {row_str}  {suffix}")


def print_eigensystem(eigenvalues: list, eigenvectors: list):
    print_section("Eigensystem")
    for k, (lam, vec) in enumerate(zip(eigenvalues, eigenvectors)):
        print(f"\n  λ{k+1} = {fmt_complex(lam)}")
        print(f"  v{k+1} = {fmt_vector(vec, fmt_complex)}")


def print_solution_table(t_values: list, solution: list, n: int):
    # Print solution as a fixed-width table.
    col_w = 14
    header_cols = ["t"] + [f"x{i+1}(t)" for i in range(n)]
    header = "  ".join(f"{h:>{col_w}}" for h in header_cols)
    print(f"\n  {header}")
    print(f"  {THIN_DIVIDER}")
    for t, x in zip(t_values, solution):
        row = "  ".join(f"{fmt_number(v):>{col_w}}" for v in [t] + x)
        print(f"  {row}")


# ─── Main flow ────────────────────────────────────────────────────────────────

def collect_inputs():
    # Interactively collect matrix A, x0, and time range from the user.

    print("\n╔══════════════════════════════════════════════╗")
    print("║        Linear ODE Solver  —  v1.0           ║")
    print("║        x′(t) = A · x(t)                     ║")
    print("╚══════════════════════════════════════════════╝")

    # Dimension
    n = read_int("\nSystem dimension (n): ")

    # Matrix A
    print(f"\nEnter matrix A row by row ({n} values per row, space-separated):")
    matrix = []
    for i in range(n):
        row = read_row(f"  Row {i+1}: ", n)
        matrix.append(row)

    # Initial conditions
    print(f"\nInitial conditions x(0)  ({n} values, space-separated):")
    x0 = read_row("  x(0): ", n)

    # Time range
    print("\nTime range:")
    t_start = read_float("  t start (default 0): " ) if prompt("  Use t=0 as start? [Y/n]: ").lower() == "n" else 0.0
    t_end   = read_float("  t end:   ")
    t_steps = read_int  ("  Number of time steps (default 50): ") if prompt("  Customise step count? [y/N]: ").lower() == "y" else 50

    return n, matrix, x0, t_start, t_end, t_steps


def ask_evaluate_points(t_values: list, solution: list, n: int):
    # After printing the table, let the user evaluate x(t) at specific
    # t values by nearest-sample lookup.
    
    print("\nEvaluate x at specific t values? [y/N]: ", end="")
    try:
        choice = input().strip().lower()
    except (KeyboardInterrupt, EOFError):
        return

    if choice != "y":
        return

    dt = t_values[1] - t_values[0] if len(t_values) > 1 else 1.0

    print("  Enter t values one per line. Press Enter on a blank line to finish.")
    while True:
        raw = prompt("  t = ")
        if raw == "":
            break
        try:
            t = float(raw)
        except ValueError:
            print("  Not a valid number.")
            continue

        idx = max(0, min(round((t - t_values[0]) / dt), len(t_values) - 1))
        t_actual = t_values[idx]
        x_actual = solution[idx]

        print(f"  t ≈ {fmt_number(t_actual)}")
        for i, v in enumerate(x_actual):
            print(f"    x{i+1} = {fmt_number(v)}")


def main():
    n, matrix, x0, t_start, t_end, t_steps = collect_inputs()

    # ── Echo inputs back ──────────────────────────────────────────────────
    print_section("Inputs")
    print_matrix(matrix, label="A")
    print(f"\n  x(0) = {fmt_vector(x0)}")
    print(f"  t ∈ [{fmt_number(t_start)}, {fmt_number(t_end)}]  —  {t_steps} steps")

    # ── Solve ─────────────────────────────────────────────────────────────
    print("\n  Solving…", end="", flush=True)
    try:
        dt       = (t_end - t_start) / max(t_steps - 1, 1)
        t_values = [t_start + i * dt for i in range(t_steps)]
        solution = solve_ode(matrix, x0, t_values)
        eigenvalues, eigenvectors = eigensystem(matrix)
    except Exception as err:
        print(f"\n\n  Error: {err}")
        sys.exit(1)
    print(" done.")

    # ── Print results ─────────────────────────────────────────────────────
    print_eigensystem(eigenvalues, eigenvectors)

    print_section(f"Solution  x(t)  —  {t_steps} samples")
    print_solution_table(t_values, solution, n)

    # ── Optional point evaluation ─────────────────────────────────────────
    ask_evaluate_points(t_values, solution, n)

    print(f"\n{DIVIDER}\n")


if __name__ == "__main__":
    main()