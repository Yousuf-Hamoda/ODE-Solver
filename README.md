# ODE Solver (In Progress)

A Python-based tool for solving systems of ordinary differential equations (ODEs), currently under active development.

## What I'm building

This project aims to provide a command-line solver for linear ODE systems with constant coefficients. The solver will:

- Accept user input for the system's order and coefficients
- Compute characteristic polynomials via matrix determinants
- Find eigenvalues and construct general solutions
- Support initial value problems (planned)

At this stage, the core determinant calculation is implemented, and work on the differential equation logic has begun.

## Current status

- `determinant.py`: Recursive determinant and cofactor expansion working for any matrix size
- `diff_eqn.py`: Partial implementation of characteristic polynomial extraction (incomplete)
- `main.py`: Basic CLI for input and determinant demo

## Next steps

- Complete the characteristic polynomial routine
- Implement eigenvalue solving
- Generate symbolic ODE solutions

Stay tuned!