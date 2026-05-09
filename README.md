# Linear ODE Solver

> **v1 — Python terminal solver is complete. React web interface is currently in progress.**

A zero-dependency ODE solver in pure Python that resolves linear systems of ordinary differential equations using Linear Algebra, with no reliance on NumPy or SciPy.

---

## How It Works

Given a linear system of the form:

```
x′(t) = A · x(t),    x(0) = x₀
```

the solver finds the exact solution using three stages of pure linear algebra:

1. **Newton's Divided Difference Interpolation** — samples `det(A − λI)` at `n+1` points and interpolates to recover the coefficients of the characteristic polynomial. No symbolic algebra is needed.

2. **Durand-Kerner Root Finding** — finds all roots of the characteristic polynomial (including complex conjugate pairs) using the Weierstrass iteration method, converging to all eigenvalues simultaneously.

3. **Eigenvector Decomposition** — for each eigenvalue `λₖ`, solves `(A − λₖI)v = 0` via Gaussian elimination to find the corresponding eigenvector. The general solution is then assembled as:

```
x(t) = c₁v₁e^(λ₁t) + c₂v₂e^(λ₂t) + ... + cₙvₙe^(λₙt)
```

The constants `c₁ … cₙ` are solved by applying the initial condition `x(0) = x₀`.

---

## Roadmap

| Feature | Status |
|---|---|
| Determinant via cofactor expansion | ✅ Complete |
| Characteristic polynomial via Newton interpolation | ✅ Complete |
| Eigenvalue finding via Durand-Kerner | ✅ Complete |
| Eigenvector solving via Gaussian elimination | ✅ Complete |
| Terminal interface (`main.py`) | ✅ Complete |
| Flask REST API (`api.py`) | ✅ Complete |
| React web frontend | 🚧 In Progress |

---

## v1 — Terminal Usage

No external libraries required. Python 3.10+ only (uses `match` statements internally).

**Run the solver:**

```bash
python main.py
```

You will be prompted to enter:
- The system dimension `n`
- The `n×n` matrix `A` row by row
- The initial condition vector `x(0)`
- A time range and number of steps

**Example session — 2×2 damped system:**


**Example output:**


---

## Web Interface (In Progress)

The web frontend is a React + Vite app that connects to the Python solver via a local Flask API.

**To run the API backend:**

```bash
pip install flask flask-cors
python api.py          # starts on http://localhost:5050
```

**To run the React frontend (once complete):**

```bash
cd web-server
npm install
npm run dev            # starts on http://localhost:3000
```

The frontend will feature a matrix input grid, interactive solution chart, eigenvalue display, and point evaluation at specific `t` values.

---

## Dependencies

| Layer | Dependencies |
|---|---|
| Python solver | None — pure Python 3.10+ stdlib only |
| Flask API | `flask`, `flask-cors` |
| React frontend | `react`, `chart.js`, `vite` |