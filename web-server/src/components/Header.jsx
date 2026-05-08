import React from 'react'

/**
 * Header
 * Displays the equation label, title, and subtitle.
 * Purely presentational — no props needed.
 */
export default function Header() {
  return (
    <header style={{ marginBottom: 28 }}>
      <p style={{
        fontFamily: 'var(--mono)',
        fontSize: 11,
        color: 'var(--accent)',
        letterSpacing: 2,
        marginBottom: 6,
        textTransform: 'uppercase',
      }}>
        x′(t) = A · x(t)
      </p>

      <h1 style={{
        fontSize: 26,
        fontWeight: 600,
        color: 'var(--text)',
        letterSpacing: -0.5,
      }}>
        Linear ODE Solver
      </h1>

      <p style={{ color: 'var(--muted)', fontSize: 14, marginTop: 4 }}>
        Eigendecomposition · no external libraries · pure Python backend
      </p>
    </header>
  )
}
