import React from 'react'

/**
 * SolveButton
 * Full-width primary action button.
 *
 * Props:
 *   onClick  — called when the user clicks
 *   loading  — boolean; shows a loading label and disables the button
 */
export default function SolveButton({ onClick, loading }) {
  return (
    <button
      onClick={onClick}
      disabled={loading}
      style={{
        width: '100%',
        padding: '13px 0',
        borderRadius: 'var(--radius-md)',
        fontSize: 15,
        fontWeight: 600,
        background: loading ? 'var(--surface2)' : 'var(--accent)',
        color: loading ? 'var(--muted)' : '#0d0f14',
        marginBottom: 24,
        letterSpacing: 0.3,
        opacity: loading ? 0.7 : 1,
        transition: 'opacity 0.2s, background 0.2s',
      }}
    >
      {loading ? 'Solving…' : 'Solve System'}
    </button>
  )
}
