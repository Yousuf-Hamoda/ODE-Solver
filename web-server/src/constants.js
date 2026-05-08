// ─── API ──────────────────────────────────────────────────────────────────
export const API_BASE = 'http://localhost:5050'

// ─── Chart colors (one per state variable) ────────────────────────────────
export const SERIES_COLORS = [
  '#6c8dfa', // blue
  '#34d399', // green
  '#f59e0b', // amber
  '#f87171', // red
  '#a78bfa', // violet
  '#38bdf8', // sky
  '#fb923c', // orange
  '#e879f9', // fuchsia
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
