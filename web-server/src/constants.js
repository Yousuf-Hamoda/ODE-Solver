// ─── API ──────────────────────────────────────────────────────────────────
export const API_BASE = ''

// ─── Chart colors (one per state variable) ────────────────────────────────
export const SERIES_COLORS = [
  '#c9a84c', // gold
  '#2ecc71', // emerald
  '#e67e22', // amber
  '#e74c3c', // red
  '#9b59b6', // purple
  '#3498db', // blue
  '#f39c12', // orange
  '#1abc9c', // teal
]

// ─── Preset ODE systems ───────────────────────────────────────────────────
//  Each preset has:
//    label  — button text
//    A      — coefficient matrix (n×n)
//    x0     — initial condition vector (length n)
export const PRESETS = [
  {
    label: 'Damped',
    A:  [[0, 1], [-2, -3]],
    x0: [1, 0],
  },
  {
    label: 'Oscillator',
    A:  [[0, 1], [-1, 0]],
    x0: [1, 0],
  },
  {
    label: '3-D Spiral',
    A:  [[-1, 2, 0], [-2, -1, 0], [0, 0, -0.5]],
    x0: [1, 0, 1],
  },
]
