"""
api.py  –  Flask REST API for the ODE solver.
Exposes POST /solve  { matrix, x0, t_start, t_end, t_steps }
Returns eigenvalues, eigenvectors, and x(t) solution data.
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS

from services.linalg import solve_ode, eigensystem
from services.polynomial import char_poly_coeffs
from services.root_solver import find_roots, clean_roots

app = Flask(__name__)
CORS(app)

# ── Security limits for public deployment ──────────────────────────────────
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024  # 64 KB max request body

# Maximum allowed matrix dimension (prevents abuse)
MAX_DIM = 8


def fmt_complex(z):
    """Serialize a complex number as {re, im}."""
    return {"re": round(z.real, 8), "im": round(z.imag, 8)}


@app.route("/solve", methods=["POST"])
def solve():
    try:
        body = request.get_json(force=True)
        A   = body["matrix"]        # list[list[float]]
        x0  = body["x0"]            # list[float]
        t_start = float(body.get("t_start", 0))
        t_end   = float(body.get("t_end",   10))
        t_steps = int(body.get("t_steps",  200))

        n = len(A)
        if any(len(row) != n for row in A):
            return jsonify({"error": "Matrix must be square"}), 400
        if len(x0) != n:
            return jsonify({"error": "x0 must match matrix dimension"}), 400
        if n < 2 or n > MAX_DIM:
            return jsonify({"error": f"Matrix dimension must be between 2 and {MAX_DIM}"}), 400

        # Time points
        dt = (t_end - t_start) / max(t_steps - 1, 1)
        t_values = [t_start + i * dt for i in range(t_steps)]

        # Eigensystem
        eigenvalues, eigenvectors = eigensystem(A)

        # Solution at each t
        solution = solve_ode(A, x0, t_values)

        return jsonify({
            "t": t_values,
            "x": solution,                          # list[list[float]]
            "eigenvalues": [fmt_complex(e) for e in eigenvalues],
            "eigenvectors": [
                [fmt_complex(c) for c in v] for v in eigenvectors
            ],
        })

    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)